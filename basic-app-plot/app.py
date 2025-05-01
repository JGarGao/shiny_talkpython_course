from shiny.express import ui, render, input
from shiny import reactive
from pathlib import Path
import pandas as pd
from shinywidgets import render_plotly
import plotly.express as px
import time

file_path = Path(__file__).parent / "penguins.csv"

df = pd.read_csv(file_path)
print(df)

@reactive.calc
@reactive.event(input.btn, ignore_none=False)
def filtered_df():
    print("executirng")
    time.sleep(1)
    return df[(df["species"].isin(input.select_species())) & (df["body_mass_g"] > input.mass())].head(input.n())

@reactive.effect()
@reactive.event(input.update)
def update_label():
    ui.update_checkbox_group("select_species", label=input.new_label())

ui.h1("Basic App")

with ui.sidebar(bg="#f8f8f8"):  
    ui.input_slider("n", "Cambia pinguinos!", 0, 350, 200)
    ui.input_numeric("mass", "Mass", 0)
    # ui.input_select("species", "Select species", list(df["species"].unique()))
    ui.input_checkbox_group("select_species", "Show Species", list(df["species"].unique()),selected=list(df["species"].unique()))
    ui.input_action_button("btn", "Submit", class_="btn-success")
    ui.input_text("new_label", "New label")
    ui.input_action_button("update", "Update")

with ui.layout_columns():

    with ui.card():

        "Plit Plot Plat"

        @render_plotly
        def plot():
        #    filtered_df = df[(df["species"]==input.species()) & (df["body_mass_g"] > input.mass())].head(input.n())
            # print(df["species"].unique())   
            # filtered_df = df[(df["species"].isin(input.select_species())) & (df["body_mass_g"] > input.mass())].sort_values(["body_mass_g"], ascending=[False]).head(input.n())
            # print(filtered_df["species"].unique())
            if input.show_species():
                return px.scatter(
                    filtered_df().sort_values(["body_mass_g"], ascending=[False]), x="bill_length_mm", y="bill_depth_mm", color="species", color_discrete_sequence=px.colors.qualitative.Vivid
                )
            else:
                return px.scatter(
                    filtered_df().sort_values(["body_mass_g"], ascending=[False]), x="bill_length_mm", y="bill_depth_mm"
                )

        ui.input_checkbox("show_species", "Show Species", value=True)

    with ui.card():

        "Peaso de tabla"

        @render.data_frame
        def render_df():
            # n = input.n()
            # mass = input.mass()
            # return df[(df["species"].isin(input.select_species())) & (df["body_mass_g"] > mass)].head(n)
            return filtered_df()




