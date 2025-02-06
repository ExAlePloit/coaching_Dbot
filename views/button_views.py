import uuid

import discord
import re
from discord import ButtonStyle, ui


class CoachingPostView(ui.View):
    def __init__(self, post_uuid: uuid.UUID):
        super().__init__(timeout=None)
        self.add_item(AcceptCoachingPostButton(post_uuid))
        # the other buttons
        # self.add_item(AcceptCoachingButton(coach_id))
        # self.add_item(AcceptCoachingButton(coach_id))


class AcceptCoachingPostButton(discord.ui.DynamicItem[discord.ui.Button],
                               template=r'coaching-post:accept(?P<post_uuid>[a-fA-F0-9-]+)'):
    def __init__(self, post_uuid: str) -> None:
        super().__init__(
            discord.ui.Button(
                label='Accept Coaching',
                style=ButtonStyle.green,
                custom_id=f'coaching-post:accept{post_uuid}',
                emoji='\N{THUMBS UP SIGN}',
            )
        )
        self.post_uuid = post_uuid

    # This is called when the button is clicked and the custom_id matches the template.
    @classmethod
    async def from_custom_id(cls, interaction: discord.Interaction, item: discord.ui.Button, match: re.Match[str], /):
        post_uuid = match['post_uuid']
        return cls(post_uuid)

    # not necessary
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Only allow the user who created the button to interact with it.
        # return interaction.user.id == self.user_id
        return True

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('Coach booked!', ephemeral=True)
