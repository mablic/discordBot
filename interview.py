import random

interview = [
'Tell me about a time when you had to work with someone who was difficult to get along with. How did you handle the situation?',
'Describe a situation where you had to make a difficult decision.',
'Tell me about a time when you had to adapt to a new situation.',
'Can you give me an example of a time when you had to work under pressure?',
'Describe a project or accomplishment that you are most proud of.',
'Tell me about a time when you had to use your analytical skills to solve a problem.',
'Describe a time when you had to persuade someone to see things your way.',
'Tell me about a time when you had to meet a tight deadline.',
'Describe a time when you had to overcome a significant obstacle to achieve a goal.',
'Tell me about a time when you had to work with a team to achieve a common goal.',
'Describe a time when you had to resolve a conflict with a coworker or classmate.',
'Tell me about a time when you had to take initiative and lead a project.',
'Describe a time when you had to learn a new skill or subject quickly.',
'Tell me about a time when you had to deal with a difficult customer or client.',
'Describe a time when you had to use your creativity to solve a problem.',
'Tell me about a time when you had to prioritize multiple tasks or projects.',
'Describe a time when you had to work with someone from a different background or culture.',
'Tell me about a time when you had to work on a project with limited resources.',
'Describe a time when you had to take on additional responsibilities or roles.',
'Tell me about a time when you had to handle a sensitive or confidential situation.',
'Describe a time when you had to make a compromise.',
'Tell me about a time when you had to handle a crisis or emergency situation.',
'Describe a time when you had to work with a supervisor who had a different management style than you.',
'Tell me about a time when you had to deal with a challenging task or project.',
'Describe a time when you had to work with a group to achieve a difficult goal.',
'Tell me about a time when you had to take constructive feedback and make improvements.',
'Describe a time when you had to delegate tasks to others.',
'Tell me about a time when you had to resolve a disagreement with a coworker or classmate.',
'Describe a time when you had to work with a team member who was not pulling their weight.',
'Tell me about a time when you had to learn from a mistake or failure.',
'Describe a time when you had to handle a difficult situation with a client or customer.',
'Tell me about a time when you had to adapt to a new system or process.',
'Describe a time when you had to take on a task or project that was outside of your comfort zone.',
'Tell me about a time when you had to work with a group to complete a project on time and within budget.',
'Describe a time when you had to overcome a challenge in order to succeed.',
'Tell me about a time when you had to manage conflicting priorities.',
'Describe a time when you had to work with a coworker or classmate who had a different work style than you.',
'Tell me about a time when you had to work on a project that required you to think outside the box.',
'Describe a time when you had to work with a team to overcome a major obstacle.',
'Describe a time when you had to manage a tight budget.',
'Tell me about a time when you had to handle a delicate situation with diplomacy.',
'Describe a time when you had to go above and beyond to deliver excellent work.',
'Tell me about a time when you had to work with a difficult supervisor or professor.',
'Describe a time when you had to take ownership of a mistake.',
'Tell me about a time when you had to navigate conflicting priorities.',
'Describe a time when you had to resolve a problem using data.',
'Tell me about a time when you had to work with a team to achieve a challenging goal.',
'Describe a time when you had to take a risk and try something new.',
'Tell me about a time when you had to be resourceful to solve a problem.',
'Describe a time when you had to work with a team that was not functioning well.',
'Tell me about a time when you had to learn a new technical skill.',
'Describe a time when you had to communicate a complex idea to someone outside your field.',
'Tell me about a time when you had to manage a difficult project or task.',
'Describe a time when you had to work with someone who had a different perspective from yours.',
'Tell me about a time when you had to manage a project with multiple stakeholders.',
'Describe a time when you had to handle a difficult customer or client who was upset.',
'Tell me about a time when you had to work with a tight deadline and limited resources.',
'Describe a time when you had to overcome a challenge related to communication.',
'Tell me about a time when you had to motivate a team to achieve a goal.',
'Describe a time when you had to make a difficult ethical decision.',
'Tell me about a time when you had to handle a conflict within a team or group.',
'Describe a time when you had to work with a difficult coworker or classmate.',
'Tell me about a time when you had to make a decision with limited information.',
'Describe a time when you had to use your problem-solving skills to resolve a difficult situation.',
'Tell me about a time when you had to take the initiative to make a change.',
'Describe a time when you had to work with a diverse group of people.',
'Tell me about a time when you had to handle a difficult customer service situation.',
'Describe a time when you had to manage a project with a tight budget.',
'Tell me about a time when you had to work with someone who had a different personality from yours.',
'Describe a time when you had to negotiate a difficult situation.',
'Tell me about a time when you had to collaborate with someone outside your field.',
'Describe a time when you had to navigate a complex project with multiple moving parts.',
'Tell me about a time when you had to handle a mistake made by a coworker or classmate.',
'Describe a time when you had to handle a situation that required you to be creative.',
'Tell me about a time when you had to handle a situation that required you to be patient.',
'Describe a time when you had to handle a situation that required you to be adaptable.',
'Tell me about a time when you had to handle a situation that required you to be a leader.',
'Describe a time when you had to handle a situation that required you to be a team player.',
'Tell me about a time when you had to handle a situation that required you to be resilient.',
'Describe a time when you had to handle a situation that required you',
'Tell me about a time when you had to handle a difficult customer service situation.',
'Describe a time when you had to use your analytical skills to solve a problem.',
'Tell me about a time when you had to work with someone who had a different work style from yours.',
'Describe a time when you had to prioritize tasks to meet a deadline.',
'Tell me about a time when you had to adapt to a new situation quickly.',
'Describe a time when you had to handle a situation that required you to be a good listener.',
'Tell me about a time when you had to handle a situation that required you to be detail-oriented.',
'Describe a time when you had to handle a situation that required you to be organized.',
'Tell me about a time when you had to handle a situation that required you to be proactive.',
'Describe a time when you had to handle a situation that required you to be patient.',
'Tell me about a time when you had to handle a situation that required you to be persuasive.',
'Describe a time when you had to handle a situation that required you to be persuasive.',
'Tell me about a time when you had to handle a situation that required you to be collaborative.',
'Describe a time when you had to handle a situation that required you to be innovative.',
'Tell me about a time when you had to handle a situation that required you to be empathetic.',
'Describe a time when you had to handle a situation that required you to be assertive.',
'Tell me about a time when you had to handle a situation that required you to be flexible.',
'Describe a time when you had to handle a situation that required you to be diplomatic.',
'Tell me about a time when you had to handle a situation that required you to be decisive.',
'Describe a time when you had to handle a situation that required you to be reliable.',
'Tell me about a time when you had to handle a situation that required you to be innovative.',
'Describe a time when you had to handle a situation that required you to be creative.',
'Tell me about a time when you had to handle a situation that required you to be a problem-solver.',
'Describe a time when you had to handle a situation that required you to be a critical thinker.',
'Tell me about a time when you had to handle a situation that required you to be a strategic planner.',
'Describe a time when you had to handle a situation that required you to be a risk-taker.',
'Tell me about a time when you had to handle a situation that required you to be a decision-maker.',
'Describe a time when you had to handle a situation that required you to be a motivator.',
'Tell me about a time when you had to handle a situation that required you to be a problem-preventer.',
'Describe a time when you had to handle a situation that required you to be a delegator.',
'Tell me about a time when you had to handle a situation that required you to be a coach.',
'Describe a time when you had to handle a situation that required you to be a teacher.',
'Tell me about a time when you had to handle a situation that required you to be a mentor.',
'Describe a time when you had to handle a situation that required you to be a learner.',
'Tell me about a time when you had to handle a situation that required you to be a listener.',
'Describe a time when you had to handle a situation that required you to be a communicator.',
'Describe a time when you had to handle a situation that required you to be a team player.',
'Tell me about a time when you had to handle a situation that required you to be a leader.',
'Describe a time when you had to handle a situation that required you to be a follower.',
'Tell me about a time when you had to handle a situation that required you to take initiative.',
'Describe a time when you had to handle a situation that required you to take ownership of a project.',
'Tell me about a time when you had to handle a situation that required you to work under pressure.',
'Describe a time when you had to handle a situation that required you to be adaptable to change.',
'Tell me about a time when you had to handle a situation that required you to work with a difficult coworker.',
'Describe a time when you had to handle a situation that required you to work with a diverse team.',
'Tell me about a time when you had to handle a situation that required you to learn a new skill quickly.',
'Describe a time when you had to handle a situation that required you to work with a limited budget.',
'Tell me about a time when you had to handle a situation that required you to work with a tight deadline.',
'Describe a time when you had to handle a situation that required you to work with a difficult customer.',
'Tell me about a time when you had to handle a situation that required you to multitask.',
'Describe a time when you had to handle a situation that required you to prioritize conflicting demands.',
'Tell me about a time when you had to handle a situation that required you to negotiate with others.',
'Describe a time when you had to handle a situation that required you to balance multiple responsibilities.',
'Tell me about a time when you had to handle a situation that required you to work independently.',
'Describe a time when you had to handle a situation that required you to work in a team with different personality types.',
'Tell me about a time when you had to handle a situation that required you to manage your time effectively.',
'Describe a time when you had to handle a situation that required you to manage conflict.',
'Tell me about a time when you had to handle a situation that required you to think creatively to solve a problem.',
'Describe a time when you had to handle a situation that required you to use your communication skills to build relationships.',
'Tell me about a time when you had to handle a situation that required you to work with minimal supervision.',
'Describe a time when you had to handle a situation that required you to learn a new technology or software.',
'Tell me about a time when you had to handle a situation that required you to be detail-oriented while managing multiple tasks.',
'Describe a time when you had to handle a situation that required you to take feedback and adjust your approach accordingly.',
'Tell me about a time when you had to handle a situation that required you to take responsibility for a mistake.',
'Describe a time when you had to handle a situation that required you to learn from failure and improve.',
'Tell me about a time when you had to handle a situation that required you to manage ambiguity and uncertainty.',
'Describe a time when you had to handle a situation that required you to navigate a complex or challenging situation.',
'Tell me about a time when you had to handle a situation that required you to work with a limited amount of resources.'
]

class Interview:

    def __init__(self):
        self.seed = set()
    
    def get_bp_questions(self):
        newQuestion = random.randint(0, len(interview))
        if len(self.seed) >= len(interview):
            self.seed = set()
        while newQuestion in self.seed and len(self.seed) < len(interview):
            # print(f"Your quesiton NO is: {newQuestion}. Duplicate from the list")
            newQuestion = random.randint(0, len(interview))
        self.seed.add(newQuestion)
        return interview[newQuestion]

    def __del__(self):
        # print(self.seed)
        pass


if __name__ == '__main__':

    pass
    # c = Interview()
    # print(c.get_bp_questions())
    # print(c.get_bp_questions())
    # print(c.get_bp_questions())
    # print(c.get_bp_questions())
    # print(c.get_bp_questions())
    # print(c.get_bp_questions())
    # print(c.get_bp_questions())
    # print(c.get_bp_questions())
    # print(c.get_bp_questions())
    # print(c.get_bp_questions())
    # print(c.get_bp_questions())
    # print(c.get_bp_questions())
    # print(c.get_bp_questions())
    # print(c.get_bp_questions())
    # print(c.get_bp_questions())