# Facebook-hackathon

Our submission for https://fbmessaging2.devpost.com/

The demonstration video can be seen here! https://vimeo.com/431949238

Any API keys in the code are now deprecated! It's easier to leave them in and preserve the git history.


## Inspiration
Wanted to offer a low level support for those struggling with mental health to make it as easy as possible for people to find solutions to their issues. Speaking to external sources such as a GP or referring into a Psychological service can be intimidating for those who need a little advice with day to day things, so our service combats this.

## What it does
- Offers easy to try solutions to day to day problems associated with mental health concerns such as stress/anxiety, depression. 
- Acts as a first point of call to reduce the cause of the stressor and improve quality of life. 
- Also offers external help sources such as anxiety support charities for those who need further support and don’t know where to turn. Provides validation to encourage people ask for help.

## How we built it
> We used python so we could rapidly prototype our idea, using the fastapi library to handle web requests and wit.ai to understand the users situation. There are 3 NLP models to determine how the user is feeling, the first to see if their initial message is positive or negative then a coarse classifier to determine whether they are stressed / depressed / lonely and then a final model to determine a specific symptom such as tiredness. The project was hosted on Heroku with automatic deployment from GitHub to make server management as easy as possible. Ideas were generated and stored with GitHub projects letting the team sort concepts and track progress. A focus on rapid prototyping was made, changing code and instantly seeing the effect in messenger.

## Challenges we ran into
- Understanding how the messenger API will interact with our project
- Understanding how our users will use the project, how they may use it is different to how we imagine
- Wit.ai training struggled with multiple similar intents
- Running our code on a remote system due to messenger API requirements meant understanding issues was harder and a very iterative process
- Managing all the possible paths the conversation can go down cleanly within our code

## Accomplishments that we're proud of
- Since the bot interprets natural language it allows an individual to feel like the system is listening to them more so than just going through multiple choice questions.
- Good use of multiple talents/backgrounds
- People we spoke too regarded the idea highly, especially if they suffered from minor anxiety and felt they wouldn’t seek professional help since it was wasting someone's time

## What we learned
- Using a large API, how information flow is handled
- How to handle sensitive user data
- Importance of continually testing the application
- Team co-ordination to generate ideas and implement our application, especially in terms of code as none of us have coded in a team before

## What's next for no problem too small
- Make the user experience more personal
- Focus on user experience improvement if they come back, tracking what they're tried and their mood, there's a lot of potential to help the user more if we can build on our previous suggestions.
- Potential survey to get a much wider range of answers to questions to improve Wit.ai training.


## Competition links

[messenger-comp](https://fbmessaging2.devpost.com/?ref_content=online-hackathons&ref_feature=challenge&ref_medium=facebook-channel)
> Create a messenger bot experiance
> Messenger comp requires at least one of Handover Protocol, One-Time Notifications, Private Replies, and Quick Replies.

[ai-comp](https://fbai2.devpost.com/?ref_content=online-hackathons&ref_feature=challenge&ref_medium=facebook-channel)
> requires use of wit.ai

**deadlines are both 24th June**

## Resources

### ai comp

- [wit.ai](https://wit.ai)
- [pywit](https://github.com/wit-ai/pywit)
- [pywit w/messenger example](https://github.com/wit-ai/pywit/blob/master/examples/messenger.py)

--- 

### messenger comp
- [One time notification documentation](https://developers.facebook.com/docs/messenger-platform/send-messages/one-time-notification/)
- [getting started with messenger bot api](https://developers.facebook.com/docs/messenger-platform/getting-started)
- [pymessenger, may not need this..](https://github.com/davidchua/pymessenger)


---

## Setup

following env variables must be set
- WEB_CONCURRENCY=1

### High level concept

Q1: How are you doing?
A1: Good -> have a great day!
A2: Not great -> Go to Q2

Q2: Whats up buttercup?
A1: I feel like too much is going on? -> Q3
A2: I just lost a close relative -> Q4

Q3: Have you tried meditating or getting some fresh air?
A1: Yes, I still feel down -> Q4
A2: No, let me give that a try! -> Great, stay safe and enjoy the outdoors, I suggest trying someone like headspace.

Q4: Have you been able to speak with anyone about this?
