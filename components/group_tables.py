from pandas.core import series

import data
from helper import format_group_odds, style_group_table
import streamlit as st
import random

def display_group_tables(group_odds, show_change=False):
    formatted = format_group_odds(group_odds)
    groups_list = list(formatted.keys())

    for i in range(0, len(groups_list), 3):
        cols = st.columns(3)

        for j in range(3):
            if i + j < len(groups_list):
                group = groups_list[i + j]

                with cols[j]:
                    st.markdown(f"### Group {group}")

                    df = formatted[group].copy()

                    if show_change:
                        df["Change (%)"] = (
                                df["Qualification %"]
                                - df["Team"].map(data.team_chances)
                        ).round(1)

                    styler_obj = style_group_table(df)

                    st.dataframe(
                        styler_obj,
                        hide_index=True,
                        use_container_width=True,
                        column_config={
                            col: st.column_config.NumberColumn(format="%.1f")
                            for col in styler_obj.data.select_dtypes(include=["float"]).columns
                        }
                    )