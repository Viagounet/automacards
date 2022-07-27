import dash_mantine_components as dmc
from dash import html, dcc


def create_timeline(state=0):
    return dmc.Timeline(
        active=1,
        bulletSize=15,
        lineWidth=2,
        children=[
            dmc.TimelineItem(
                title="Register on AutomaCard",
                children=[
                    dmc.Text(
                        [
                            "You already did the hardest part! Now it's up to you ",
                            dmc.Anchor("to get started", href="#", size="sm"),
                            " with your learning adventure!",
                        ],
                        color="dimmed",
                        size="sm",
                    ),
                ],
            ),
            dmc.TimelineItem(
                title="Create your first card",
                children=[
                    dmc.Text(
                        [
                            "You've created your ",
                            dmc.Anchor("first card!", href="#", size="sm"),
                        ],
                        color="dimmed",
                        size="sm",
                    ),
                ],
            ),
            dmc.TimelineItem(
                title="Take a test",
                lineVariant="dashed",
                children=[
                    dmc.Text(
                        [
                            "Feeling ready to test your skills? ",
                            dmc.Anchor(
                                "Take your first test!",
                                href="#",
                                size="sm",
                            ),
                        ],
                        color="dimmed",
                        size="sm",
                    ),
                ],
            ),
            dmc.TimelineItem(
                [
                    dmc.Text(
                        [
                            dmc.Anchor(
                                "Levels",
                                href="https://github.com/AnnMarieW",
                                size="sm",
                            ),
                            " are a proof of your progress, try reaching level 5!",
                        ],
                        color="dimmed",
                        size="sm",
                    ),
                ],
                title="Reach global level 5",
            ),
        ],
    )
