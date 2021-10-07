
class TopicRequestMessage():

    def __init__(self, members, sentences):
        self.members = members
        self.sentences = sentences

    def setMemberId(self, memberId):
        self.memberId = memberId
    
    def setMembers(self, members):
        self.members = members

    def setSentences(self, sentences):
        self.sentences = sentences

class TopicResponseMessage():

    def __init__(self, members, topics):
        self.members = members
        self.topics = topics

    def setMemberId(self, memberId):
        self.memberId = memberId
    
    def setMembers(self, members):
        self.members = members

    def setSentences(self, topics):
        self.topics = topics