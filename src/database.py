from models.dev_stats import DevStats
from models.power_conditions import PowerConditions
from models.non_med_err import NonMedErrorCount
from models.write_error import WriteError
from models.read_error import ReadError
import psycopg2
import logging
import utils

def connect(database, username, password, host):
    conn = psycopg2.connect(f'dbname={database} user={username} password={password} host={host}')
    return conn

def recreate_tables(conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS drive")
    cur.execute("DROP TABLE IF EXISTS tape")
    cur.execute("CREATE TABLE drive (id serial PRIMARY KEY, log_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,   \
            drive_id VARCHAR, session_id VARCHAR, non_medium_error_count INTEGER, total_errors_corrected_read INTEGER, total_bytes_processed_read INTEGER, total_uncorrected_errors_read INTEGER, total_errors_corrected_write INTEGER, total_bytes_processed_write INTEGER, total_uncorrected_errors_write INTEGER, dev_stats JSONB, read_error JSONB, write_error JSONB)")
    cur.execute("CREATE TABLE tape (id serial PRIMARY KEY, log_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, drive_id VARCHAR, session_id INTEGER, \
                volume_serial_number TEXT, volume_barcode TEXT, volume_personality TEXT, page_valid INTEGER, thread_count INTEGER, \
                total_read_retries INTEGER, total_write_retries INTEGER, lifetime_megabytes_read INTEGER, last_mount_megabytes_read INTEGER, lifetime_megabytes_written INTEGER, last_mount_megabytes_written  INTEGER, \
                total_unrecovered_read_errors INTEGER, total_unrecovered_write_errors INTEGER, \
                volstats JSONB, tapealert JSONB, tapeusage JSONB, tapecap JSONB, sequentialaccess JSONB)")
    cur.close()
    conn.commit()

def write_to_tape_db(logs, state ,drive_id, session_id, conn):
    volStats = logs['vol_stats']
    volStats_json = logs['vol_stats'].to_json()
    tape_alert_json = logs['tape_alert'].to_json()
    tape_usage_json = logs['tape_usage'].to_json()
    tape_cap_json = logs['tape_cap'].to_json()
    seq_access_json = logs['seq_access'].to_json()
    prev_hash, curr_hash, hash_updated = state.update_tape_hash(drive_id, utils.hash_strings(volStats_json, tape_alert_json, tape_usage_json, tape_cap_json, seq_access_json))
    if hash_updated:
        logging.debug(f"TAPE Row written: {prev_hash} != {curr_hash}")
        cur = conn.cursor()
        cur.execute(f"INSERT INTO tape (drive_id, session_id, volume_serial_number, volume_barcode, volume_personality, page_valid, thread_count, \
                    total_read_retries, total_write_retries, lifetime_megabytes_read, last_mount_megabytes_read, lifetime_megabytes_written, last_mount_megabytes_written, \
                    total_unrecovered_read_errors, total_unrecovered_write_errors, \
                    volstats, tapealert, tapeusage, tapecap, sequentialaccess) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (drive_id, session_id, volStats.volume_serial_number, volStats.volume_barcode, volStats.volume_personality, volStats.page_valid, volStats.thread_count,
                    volStats.total_read_retries, volStats.total_write_retries, volStats.lifetime_megabytes_read, volStats.last_mount_megabytes_read,
                    volStats.lifetime_megabytes_written, volStats.last_mount_megabytes_written, volStats.total_unrecovered_read_errors, volStats.total_unrecovered_write_errors,
                    volStats_json, tape_alert_json,tape_usage_json, tape_cap_json, seq_access_json))
        cur.close()
        conn.commit()
    else:
        logging.debug(f"TAPE Row not written due to {prev_hash} equal to {curr_hash}")

def write_to_drive_db(logs, state, drive_id, session_id, conn):
    devStats: DevStats = logs['dev_stats']
    writeError: WriteError = logs['write_err']
    readError: ReadError = logs['read_err']
    powerConditions: PowerConditions = logs['power_conditions']
    nonMedErrorCount: NonMedErrorCount = logs['non_med_err']
    prev_hash, curr_hash, hash_updated = state.update_tape_hash(drive_id, utils.hash_strings(devStats.to_json(), writeError.to_json(), readError.to_json()))
    if hash_updated:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO drive (drive_id, session_id, non_medium_error_count, total_errors_corrected_read, total_bytes_processed_read,\
                    total_uncorrected_errors_read, total_errors_corrected_write, total_bytes_processed_write, total_uncorrected_errors_write, \
                    dev_stats, read_error, write_error) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (drive_id, session_id, nonMedErrorCount.non_medium_error_count, readError.total_errors_corrected, readError.total_bytes_processed,
                readError.total_uncorrected_errors, writeError.total_errors_corrected, writeError.total_bytes_processed, writeError.total_uncorrected_errors
                ,devStats.to_json(), readError.to_json(), writeError.to_json()))
        cur.close()
        conn.commit()
    else:
        logging.debug(f"DRIVE Row not written due to {prev_hash} equal to {curr_hash}")
