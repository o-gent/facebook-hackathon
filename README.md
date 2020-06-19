# Facebook-hackathon

The master branch is in production at [mental-heal](https://mental-heal.herokuapp.com/). Any development should be done in development branch.

Facebook submission 

1. What's your project called?
> ?

2. Here's the elevator pitch. What's your idea? This will be a short tagline for the project
> Tackle mental health problems with a messenger bot

3. What languages, APIs, hardware, hosts, libraries, UI Kits or frameworks are you using?
> Built with python using the fastapi library to handle web requests, witai for NLP and the site is served with heroku.

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
