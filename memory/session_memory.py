# stores current session data so agent can answer follow-up questions

class SessionMemory:
    def __init__(self):
        self.job_description = None
        self.resumes = []          # list of dicts {id, text, metadata}
        self.scores = {}           # resume_id -> score
        self.ranking = []          # sorted list of resume_ids
        self.chat_history = []     # list of (user_msg, agent_msg)

    def save_job_description(self, jd_text):
        self.job_description = jd_text

    def add_resume(self, resume_id, resume_text, metadata=None):
        if metadata is None:
            metadata = {}
        self.resumes.append({
            "id": resume_id,
            "text": resume_text,
            "metadata": metadata
        })

    def set_scores(self, scores_dict):
        # scores_dict = {resume_id: score}
        self.scores = scores_dict

    def set_ranking(self, ranked_ids):
        self.ranking = ranked_ids

    def get_top_candidates(self, top_n):
        return self.ranking[:top_n]

    def get_candidate_score(self, resume_id):
        return self.scores.get(resume_id, 0)

    def add_chat_turn(self, user_msg, agent_msg):
        self.chat_history.append((user_msg, agent_msg))

    def get_all_resumes(self):
        return self.resumes

    def get_job_description(self):
        return self.job_description

    def clear(self):
        self.job_description = None
        self.resumes = []
        self.scores = {}
        self.ranking = []
        self.chat_history = []

# create one memory instance per session
memory = SessionMemory()