from bokeh.io import curdoc
from bokeh.layouts import column, gridplot, row
from bokeh.models import Button, Column, ColumnDataSource, Paragraph, TabPanel
from bokeh.models.widgets import TextInput
from bokeh.plotting import figure
from campbell import campbell

address: str = "172.17.204.40"
table: str = "ASSET_1min"

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
data_source: ColumnDataSource = ColumnDataSource(data=data_format)


def update_data() -> None:
    """Updates the data source"""
    ASSET: campbell = campbell(address, [table])
    data = ASSET.data_dict(table)
    new_data: dict[str, list] = {
        "DateTime": [data["datetime"][0]],
        "Date": [data["datetime"].split("T")[0][0]],
        "Time": [data["datetime"].split("T")[1][0]],
        "WS_avg": [data["WS_avg"][0]],
        "WindDir_vct": [data["WindDir_vct"][0]],
        "AirTemp_Avg": [data["AirTemp_Avg"][0]],
        "TT_C_Avg": [data["TT_C_Avg"][0]],
        "BP_Avg": [data["BP_Avg"][0]],
        "RH_Avg": [data["RH_Avg"][0]],
        "DP_Avg": [data["DP_Avg"][0]],
        "Incoming_SW_Avg": [data["Incoming_SW_Avg"][0]],
        "Outgoing_SW_Avg": [data["Outgoing_SW_Avg"][0]],
        "Incoming_LW_Avg": [data["Incoming_LW_Avg"][0]],
        "Outgoing_LW_Avg": [data["Outgoing_LW_Avg"][0]],
        "NetSW_Avg": [data["NetSW_Avg"][0]],
        "NetLW_Avg": [data["NetLW_Avg"][0]],
        "Albedo_Avg": [data["Albedo_Avg"][0]],
        "MetSENS_Status": [data["MetSENS_Status"][0]],
        "Good_Sample_Tot": [data["Good_Sample_Tot"][0]],
        "BattV_Min": [data["BattV_Min"][0]],
    }
    data_source.stream(new_data, rollover=60 * 24)  # keep last 24 hours of data


curdoc().add_periodic_callback(update_data, 60000)  # update data every minute
# curdoc().add_root(Tabs(tabs=[mfc_tab, scale_tab], sizing_mode="stretch_both"))
