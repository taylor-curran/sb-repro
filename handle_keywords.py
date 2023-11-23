from prefect import task, flow
from auxillary import get_reduced_kw_relationship_map
from marvin import ai_fn

@ai_fn
def activation_score(message: str, keyword: str, target_relationship: str) -> float:
    """Return a score between 0 and 1 indicating whether the target relationship exists
    between the message and the keyword"""

@task
async def handle_keywords(
    message: str = "hello",
    channel_name: str = "channel_name",
    asking_user: str = "asking_user",
    link: str = "link",
):
    keyword_relationships = await get_reduced_kw_relationship_map()

    keywords = [
        keyword for keyword in keyword_relationships.keys() if keyword in message
    ]

    print("🔑 Key Words: ", keywords)

    for keyword in keywords:
        target_relationship = keyword_relationships.get(keyword)
        if not target_relationship:
            continue
        score = activation_score(message, keyword, target_relationship)
        print("⛳️ Score: ", score)
        if score > 0.5:
            print("🚀 Posting to Slack")
            message=(
                f"A user ({asking_user}) just asked a question in \n"
                f" {channel_name} that contains the keyword `{keyword}`,\n and I'm"
                f" {score*100:.0f}% sure that their message indicates the \n"
                f" following:\n\n**{target_relationship!r}**.\n\n[Go to"
                f" message]({link})"
            )
            print("\n\n📨 Message: \n\n", message, "\n")
            return

        else:
            print("🚫 Not posting to Slack")




@flow(log_prints=True)
def f_handle_keywords(message: str, channel_name: str, asking_user: str, link: str):
    handle_keywords(
        message=message,
        channel_name=channel_name,
        asking_user=asking_user,
        link=link,
    )


if __name__ == "__main__":
    f_handle_keywords(
        message="hello i am seeing a 429 error",
        channel_name="channel_name",
        asking_user="asking_user",
        link="link",
    )
