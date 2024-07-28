from bokeh.layouts import column, gridplot, row
from bokeh.models import Button, Column, ColumnDataSource, Paragraph, TabPanel
from bokeh.models.widgets import TextInput
from bokeh.plotting import figure
from campbell import campbell

address: str = "172.17.204.40"
table: str = "ASSET_1min"

ASSET = campbell(address, [table])

data_format: dict[str, list] = {
    "DateTime": [],
    "Date": [],
    "Time": [],
    "WS_avg": [],
    "WindDir_vct": [],
    "AirTemp_Avg": [],
    "TT_C_Avg": [],
    "BP_Avg": [],
    "RH_Avg": [],
    "DP_Avg": [],
    "Incoming_SW_Avg": [],
    "Outgoing_SW_Avg": [],
    "Incoming_LW_Avg": [],
    "Outgoing_LW_Avg": [],
    "NetSW_Avg": [],
    "NetLW_Avg": [],
    "Albedo_Avg": [],
    "MetSENS_Status": [],
    "Good_Sample_Tot": [],
    "BattV_Min": [],
}

# Data Source
data_source = ColumnDataSource(data=data_format)


def update_data():
    ASSET.pull_recent()
    new_data = {
        "DateTime": [],
        "Date": [],
        "Time": [],
        "WS_avg": [],
        "WindDir_vct": [],
        "AirTemp_Avg": [],
        "TT_C_Avg": [],
        "BP_Avg": [],
        "RH_Avg": [],
        "DP_Avg": [],
        "Incoming_SW_Avg": [],
        "Outgoing_SW_Avg": [],
        "Incoming_LW_Avg": [],
        "Outgoing_LW_Avg": [],
        "NetSW_Avg": [],
        "NetLW_Avg": [],
        "Albedo_Avg": [],
        "MetSENS_Status": [],
        "Good_Sample_Tot": [],
        "BattV_Min": [],
    }
    data_source.stream(new_data, rollover=100)
