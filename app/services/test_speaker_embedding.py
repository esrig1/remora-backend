import speaker_embedding

test_data = [
        {
            "start": 0.459,
            "end": 8.755,
            "speaker": "SPEAKER_01",
            "text": " Hi, I'm Rhea. Thank you for coming to interview with us today. Let's just go ahead and get started with a quick introduction. Could you tell me a little bit about yourself?"
        },
        {
            "start": 9.15,
            "end": 53.839,
            "speaker": "SPEAKER_00",
            "text": " Yeah, absolutely. First of all, thank you so much for having me. It's an honor to be here. So a bit about myself. I'm originally from Morocco, where I lived pretty much my whole life. I then came to Boston and studied industrial engineering at Northeastern University. While I was in college, I did a few different internships. I did technical ones at a local power plant and at Amazon Robotics. And I also did one in consulting at the Boston Consulting Group, and was also the president of the consulting club at my university.  So really I'm someone who enjoys both the business side of things but I also do have a passion for technology. So down the line my goal is to start my own education technology company in my home country Morocco so I can make education more affordable through the use of tech. And outside of like school and work I also do magic tricks on college campuses."
        },
        {
            "start": 54.419,
            "end": 61.546,
            "speaker": "SPEAKER_01",
            "text": "Oh wow that sounds like a very impressive background. So why exactly are you interested in interviewing with our consulting firm?"
        },
        {
            "start": 61.985,
            "end": 89.975,
            "speaker": "SPEAKER_00",
            "text": " Yeah, my reasons for joining your consulting firm are twofold. Number one, I think the exposure to the strategy work is very appealing to me. And then second, the opportunities for externship is also one that I am highly looking at. So on the strategy side, I know that your consulting firm is one of the few that gives you exposure to C-suite executives and to strategy type projects early on in your career, which is something that I won't find at other companies. Then the second reason is the opportunity to do externships. So as I mentioned, I am interested in the education sector down the line."
        }
    ]

def test_speaker_embedding():
    service = speaker_embedding.SpeakerService("", test_data)
    result = service.find_best_clips()
    print(result)


if __name__ == "__main__":
    print("Starting Tests")
    print(test_speaker_embedding())