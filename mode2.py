from landsites import Land
from data_structures.heap import MaxHeap

class Mode2Navigator:
    """
    This class simulates the operations of a number of adventurer teams raiding differnet sites (lands).
    it uses MaxHeap for most of the simulation with some lists and tuples to support for storing some temporary data.
    this class efficiently manages sites scores using max heap, ensuring the raiders always raid the land with highest score first.
    Example: after calculation potential score of every island and returning a max heap order of 400, 300, 250. Raiders will raid the land with 400 then 300 then 250 with the get max method.
    every time the land gets raided it will compute its potential score again and add back to the heap as it still can be better than other lands.
    Best case complexity results for add site is O(1) when only 1 site is added and Worst case is O(N) when there's N sites added.
    The complexity of simulate day itself is influenced by construct_score_data_structure method as it calls it initially to compute the potential scores for every site, which has a best and worst case of O(comp) and O(N*comp) respectively
    Adding the complexity above with the complexity of the method itself, which has a best case and worst case of O(comp) and O(Klog(N)*comp) respectively,
    we get the overall complexity of O(comp) for best and O(N*comp + Klog(N)*comp) for worst. 
    """

    def __init__(self, n_teams: int) -> None:
        """
            initiallizing a new object of this class with N teams
            Parameters:
                n_teams: the amount of adventure teams 
            Complexity:
                best and worst case: O(1)
        """
        self.team_count = n_teams
        self.sites = []
        self.scores = None

    def add_sites(self, sites: list[Land]) -> None:
        """
            adding all the sites and creating the max heap corresponding to the amount of sites
            Parameters:
                sites: a list of lands to be added
            Complexity
                best case: O(1), when there's only 1 site to be added
                worst case: O(N), when there's N sites to be added
        """
        for site in sites:
            self.sites.append(site)
        self.scores = MaxHeap(len(self.sites))


    def simulate_day(self, adventurer_size: int) -> list[tuple[Land | None, int]]:
        """
            simulates the day as all the teams are sent/not sent to the lands to rob gold.  Using the get max method to rob the lands with highest scores first then re-add it into our heap after.
            Parameters:
                adventurer_size: the adventurer size of every team for calculating the potential scores of every site and the score if not sending any.
            Return:
                a result which stores all the sites raided and adventurers sent on every raid.
            Complexity:
                Best case: if there's only 1 site and 1 team, it'll have a complexity of O(comp) where O(1) is to add the 1 site back into the heap and O(comp) to compare in compute score.
                Worst case: O(N*comp + Klog(N)*comp) where K is the number of teams and N is number of sites, constructing the data structure will have a complexity of O(N*comp)
                For loop runs K times as there's K teams and log(N) for add method to add the site back into the heap data structure and O(comp) to compare in compute score.
        """
        result = []
        self.construct_score_data_structure(adventurer_size)
        for teams in range(self.team_count):
            team_score, site, adventurers_remaining = self.scores.get_max()
            adventurers_sent = adventurer_size - adventurers_remaining
            reward = team_score - (2.5*adventurers_remaining)
            if adventurers_remaining == adventurer_size:
                result.append((None, adventurer_size))
            else:
                result.append((site, adventurers_sent))
            site.gold -= reward
            site.guardians -= adventurers_sent
            new_score, new_adventurers_remaining = self.compute_score(site, adventurer_size)
            self.scores.add((new_score, site, new_adventurers_remaining))
        return result

    def compute_score(self, site: Land, adventurer_size: int):
        """
            computes the potential score for the lands with the given adventurer size.
            Parameters:
                site: the current site to be calculated
                adventurer_size: the adventurer size for every team that can be sent to the site
            Returns:
                the score of the current site and the adventurers remaining 
            Complexity:
                O(comp): the complexity for comparing the scores if not sending is better or looting islands is better
        """
        default_reward = adventurer_size*2.5
        score = 0
        if site.get_guardians() > 0 and site.get_gold() > 0:
            adventurers_sent = min(adventurer_size, site.get_guardians())
            reward = min(adventurers_sent*site.get_gold()/site.get_guardians(), site.get_gold())
            adventurers_remaining = adventurer_size - adventurers_sent
            score = 2.5*adventurers_remaining + reward

        if default_reward >= score:
            return (default_reward, adventurer_size)
        else:
            return (score, adventurers_remaining)

    def construct_score_data_structure(self, adventurer_size):
        """
            constructs the max heap data structure for all the sites according to their respective scores.
            Parameters:
                adventurer_size: the adventurer size for every team that can be sent to the site
            Complexity:
                Best case: O(comp): when there's only 1 site, it only has to compute the score and heapify that one site, for loop has O(1) complexity 
                while comparing score has O(comp) complexity and heapify 1 site has O(1) complexity, making it's overall best case O(comp).
                Worst case: O(N*comp): when there's N sites, for loop runs N times, compares N times which makes the complexity O(N*comp). 
                Heapifying the score list will have a O(N) complexity aswell, making its overall worst case complexity O(N*comp) 
        """
        score_list = []
        for site in self.sites:
            score, adventurers_remaining = self.compute_score(site, adventurer_size)
            score_list.append((score, site, adventurers_remaining))

        self.scores = MaxHeap.heapify(score_list)