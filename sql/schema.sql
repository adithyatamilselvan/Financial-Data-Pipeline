CREATE DATABASE IF NOT EXISTS financial_pipeline;
USE financial_pipeline;
CREATE TABLE IF NOT EXISTS transactions (
  transaction_id VARCHAR(32) PRIMARY KEY,
  account_id VARCHAR(32) NOT NULL,
  transaction_date DATE NOT NULL,
  amount DECIMAL(14, 2) NOT NULL,
  currency CHAR(3) NOT NULL,
  amount_usd DECIMAL(14, 2),
  merchant VARCHAR(150),
  category VARCHAR(50),
  status VARCHAR(20),
  source VARCHAR(20),
  is_international BOOLEAN NOT NULL,
  transaction_month CHAR(7),
  day_of_week VARCHAR(12),
  transaction_type VARCHAR(10),
  INDEX idx_transactions_date (transaction_date),
  INDEX idx_transactions_category (category),
  INDEX idx_transactions_account (account_id)
);
CREATE TABLE IF NOT EXISTS pipeline_runs (
  run_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  started_at TIMESTAMP NOT NULL,
  completed_at TIMESTAMP NULL,
  rows_processed INT NOT NULL DEFAULT 0,
  rows_loaded INT NOT NULL DEFAULT 0,
  quality_passed BOOLEAN NOT NULL,
  status VARCHAR(20) NOT NULL,
  error_message TEXT
);
CREATE TABLE IF NOT EXISTS transaction_anomalies (
  anomaly_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  transaction_id VARCHAR(32) NOT NULL,
  anomaly_type VARCHAR(50) NOT NULL,
  details VARCHAR(255),
  detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);