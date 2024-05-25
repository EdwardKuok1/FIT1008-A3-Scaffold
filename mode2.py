from landsites import Land
from data_structures.heap import MaxHeap

class Mode2Navigator:
    """
    Student-TODO: short paragraph as per
    https://edstem.org/au/courses/14293/lessons/46720/slides/318306
    """

    def __init__(self, n_teams: int) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        self.team_count = n_teams
        self.sites = []
        self.scores = None

    def add_sites(self, sites: list[Land]) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        for site in sites:
            self.sites.append(site)
        self.scores = MaxHeap(len(self.sites))

    def simulate_day(self, adventurer_size: int) -> list[tuple[Land | None, int]]:
        """
        Student-TODO: Best/Worst Case
        """
        result = []
        self.construct_score_data_structure(adventurer_size)
        #for i in range(len(self.scores)):
        #    print(self.scores.get_max())
        for teams in range(self.team_count):
            team_score, site, adventurers_remaining = self.scores.get_max()
            print(team_score, site, adventurers_remaining)
            if adventurers_remaining == adventurer_size:
                result.append((None, adventurer_size))
            else:
                result.append((site, adventurer_size - adventurers_remaining))
            print(result[teams])
        return result

    def comupte_score(self, site: Land, adventurer_size: int):
        default_reward = adventurer_size*2.5
        score = 0
        if site.get_guardians() > 0 and site.get_gold() > 0:
            adventurers_sent = min(adventurer_size, site.get_guardians())
            reward = min(adventurers_sent*site.get_gold()/site.get_guardians(), site.get_gold())
            adventurers_remaining = adventurer_size - adventurers_sent
            score = 2.5*adventurers_remaining + reward

        if default_reward > score:
            return (default_reward, adventurer_size)
        else:
            site.gold -= reward
            site.guardians -= adventurers_sent
            return (score, adventurers_remaining)

    def construct_score_data_structure(self, adventurer_size):
        for site in self.sites:
            score, adventurers_remaining = self.comupte_score(site, adventurer_size)
            self.scores.add((score, site, adventurers_remaining))