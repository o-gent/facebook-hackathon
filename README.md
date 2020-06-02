# Facebook-hackathon

The master branch is in production at [mental-heal](https://mental-heal.herokuapp.com/). Any development should be done in development branch.

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
