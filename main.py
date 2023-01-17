import click
import requests
import tweepy

@click.command()
@click.option('--hubspot-api-key', prompt='HubSpot API Key', help='Your HubSpot API key.')
@click.option('--twitter-consumer-key', prompt='Twitter Consumer Key', help='Your Twitter Consumer Key.')
@click.option('--twitter-consumer-secret', prompt='Twitter Consumer Secret', help='Your Twitter Consumer Secret.')
@click.option('--twitter-access-token', prompt='Twitter Access Token', help='Your Twitter Access Token.')
@click.option('--twitter-access-token-secret', prompt='Twitter Access Token Secret', help='Your Twitter Access Token Secret.')
@click.option('--twitter-username', prompt='Twitter Username', help='The username of the user whose data you want to use to create a HubSpot contact.')

def create_contact(hubspot_api_key,
                   twitter_consumer_key,
                   twitter_consumer_secret,
                   twitter_access_token,
                   twitter_access_token_secret,
                   twitter_username):
    """Create a HubSpot contact based on Twitter user data."""

    # Authenticate with the Twitter API
    auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    api = tweepy.API(auth)

    # Get the Twitter user's information
    user = api.get_user(twitter_username)
    name = user.name
    email = user.email
    bio = user.description
    location = user.location

    # Create the contact in HubSpot
    url = 'https://api.hubapi.com/contacts/v1/contact'
    data = {
        "properties": [
            {
                "property": "email",
                "value": email
            },
            {
                "property": "firstname",
                "value": name.split()[0]
            },
            {
                "property": "lastname",
                "value": name.split()[1]
            },
            {
                "property": "bio",
                "value": bio
            },
            {
                "property": "location",
                "value": location
            }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {hubspot_api_key}"
    }
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        click.echo("Contact created successfully.")
    else:
        click.echo(f'Error: {response.text}')

if __name__ == '__main__':
    create_contact()
