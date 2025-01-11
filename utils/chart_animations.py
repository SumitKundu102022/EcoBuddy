import plotly.graph_objects as go

def create_animated_pie_chart(categories, footprints_frames):
    """
    Creates an animated pie chart with the given categories and frame data.

    Args:
        categories (list): List of categories for the pie chart labels.
        footprints_frames (list): List of dictionaries, each containing frame name and footprint values.

    Returns:
        go.Figure: A Plotly animated pie chart figure.
    """
    fig = go.Figure()

    # Add the initial frame (base frame)
    fig.add_trace(
        go.Pie(
            labels=categories,
            values=footprints_frames[0]["footprints"],
            name=footprints_frames[0]["frame"]
        )
    )

    # Add frames for animation
    for frame_data in footprints_frames:
        fig.add_trace(
            go.Pie(
                labels=categories,
                values=frame_data["footprints"],
                name=frame_data["frame"]
            )
        )

    # Update layout with animation settings
    fig.update_layout(
        title="Carbon Footprint Breakdown (Animated)",
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "buttons": [
                {"label": "Play", "method": "animate", "args": [None, {"frame": {"duration": 1000, "redraw": True}}]},
                {"label": "Pause", "method": "animate", "args": [[None], {"frame": {"duration": 0, "redraw": False}}]}
            ]
        }],
        sliders=[{
            "steps": [
                {"method": "animate", "label": frame_data["frame"], "args": [[frame_data["frame"]], {"frame": {"duration": 500, "redraw": True}}]}
                for frame_data in footprints_frames
            ]
        }]
    )

    # Add frames to the figure
    fig.frames = [
        go.Frame(
            data=[
                go.Pie(labels=categories, values=frame_data["footprints"])
            ],
            name=frame_data["frame"]
        )
        for frame_data in footprints_frames
    ]

    return fig
