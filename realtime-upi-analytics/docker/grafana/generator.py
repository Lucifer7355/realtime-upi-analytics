import json

def panel(title, query, panel_id, panel_type="timeseries", span=12, height=8):
    return {
        "id": panel_id,
        "title": title,
        "type": panel_type,
        "datasource": {"type": "postgres", "uid": "postgres_ds"},
        "targets": [
            {
                "rawSql": query,
                "format": "time_series",
                "refId": "A",
            }
        ],
        "gridPos": {"h": height, "w": span, "x": 0, "y": (panel_id - 1) * height},
    }


dashboard = {
    "id": None,
    "title": "UPI Analytics — Full Auto Dashboard",
    "timezone": "browser",
    "schemaVersion": 36,
    "version": 1,
    "refresh": "5s",
    "panels": [

        # ----------------------------------------------------
        # REAL-TIME PANELS
        # ----------------------------------------------------

        panel(
            "Real-Time Transactions Per Minute",
            """
            SELECT date_trunc('minute', event_time) AS time, COUNT(*)
            FROM clean_upi_transactions
            WHERE $__timeFilter(event_time)
            GROUP BY 1 ORDER BY 1;
            """,
            1
        ),

        panel(
            "Success / Failed / Pending (Live)",
            """
            SELECT status, COUNT(*)
            FROM clean_upi_transactions
            WHERE $__timeFilter(event_time)
            GROUP BY status;
            """,
            2,
            panel_type="piechart"
        ),

        panel(
            "Failures Per Minute (Spike Detector)",
            """
            SELECT date_trunc('minute', event_time) AS time,
                   SUM(CASE WHEN status='FAILED' THEN 1 ELSE 0 END)
            FROM clean_upi_transactions
            WHERE $__timeFilter(event_time)
            GROUP BY 1 ORDER BY 1;
            """,
            3
        ),

        panel(
            "UPI Transactions by Bank (payer handle)",
            """
            SELECT split_part(payer, '@', 2) AS bank,
                   COUNT(*)
            FROM clean_upi_transactions
            WHERE $__timeFilter(event_time)
            GROUP BY 1 ORDER BY COUNT(*) DESC LIMIT 10;
            """,
            4,
            panel_type="barchart"
        ),

        # ----------------------------------------------------
        # DAILY SUMMARY PANELS
        # ----------------------------------------------------

        panel(
            "Daily Total Transactions",
            """
            SELECT date AS time, total_txns
            FROM daily_upi_summary
            WHERE $__timeFilter(date)
            ORDER BY date;
            """,
            5
        ),

        panel(
            "Daily Success vs Failed vs Pending",
            """
            SELECT date AS time,
                   success_txns,
                   failed_txns,
                   pending_txns
            FROM daily_upi_summary
            WHERE $__timeFilter(date)
            ORDER BY date;
            """,
            6
        ),

        panel(
            "Daily Total Amount Processed",
            """
            SELECT date AS time, total_amount
            FROM daily_upi_summary
            WHERE $__timeFilter(date)
            ORDER BY date;
            """,
            7
        ),

        # ----------------------------------------------------
        # MERCHANT ANALYTICS PANELS
        # ----------------------------------------------------

        panel(
            "Top 10 Merchants (Today)",
            """
            SELECT merchant, SUM(total_txns)
            FROM merchant_upi_summary
            WHERE date = CURRENT_DATE
            GROUP BY merchant
            ORDER BY SUM(total_txns) DESC
            LIMIT 10;
            """,
            8,
            panel_type="barchart"
        ),

        panel(
            "Merchant Transaction Trend",
            """
            SELECT date AS time, SUM(total_txns)
            FROM merchant_upi_summary
            WHERE $__timeFilter(date)
            GROUP BY date
            ORDER BY date;
            """,
            9
        ),

        panel(
            "Merchant Amount Trend",
            """
            SELECT date AS time, SUM(amount)
            FROM merchant_upi_summary
            WHERE $__timeFilter(date)
            GROUP BY date
            ORDER BY date;
            """,
            10
        ),

        # ----------------------------------------------------
        # HEATMAPS
        # ----------------------------------------------------

        panel(
            "Hourly Transaction Heatmap",
            """
            SELECT 
                date_trunc('hour', event_time) AS time,
                COUNT(*) AS volume
            FROM clean_upi_transactions
            WHERE $__timeFilter(event_time)
            GROUP BY 1 ORDER BY 1;
            """,
            11,
            panel_type="heatmap"
        ),

        panel(
            "Hourly Amount Heatmap",
            """
            SELECT 
                date_trunc('hour', event_time) AS time,
                SUM(amount) AS total_amount
            FROM clean_upi_transactions
            WHERE $__timeFilter(event_time)
            GROUP BY 1 ORDER BY 1;
            """,
            12,
            panel_type="heatmap"
        ),
    ]
}

with open("upi_dashboard_full.json", "w") as f:
    json.dump(dashboard, f, indent=2)

print("FULL UPI Dashboard generated!")
