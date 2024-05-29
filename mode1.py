from landsites import Land
from data_structures.bst import BinarySearchTree

class Mode1Navigator:
    """
    This class manages a list of 'land' and a specified number of adventurers and returns the max amount of gold that can be made, simulating different adventure scenarios and updating site details.
    The data structures used consists of BinarySearchTree and some list and tuples for support to store temporary data.
    The BST sorts and stores 'land' objects based on their guardians to gold ratio, which ensures the efficient retrieval and updating of sites.
    Example: 
        If the number of guardians stationed on the sites goes by the order [300, 100, 150, 50] and the adventurers given are 500. Then the adventurers will be split into 300, 100, 100 to raid the sites.
    Complexity:
        Initialization:
            Best Case: O(log(N)) where N is the number of sites, if adding one site to an already balanced BST.
            Worst Case: O(Nlog(N)) for N sites, where each insertion into the BST takes O(log(N)) and this is repeated N times.
        select_sites:
            Best Case: O(log(N)) if only one route is chosen in the BST
            Worst Case: O(N) if the number of guardians in all sites is less than the number of adventurers, requiring traversal of all N nodes.
        select_sites_from_adventurer_numbers:
            Best Case: O(logN), when theres only 1 adventure number and 1 list to calculate, the bst only chooses 1 route which has a complexity of log(N) when theres N sites.
            Worst Case: O(N*M) where N is the number of sites and M is the number of adventure numbers, with the outer loop running M times and the inner loop running N times
        update_site:
            Best and Worst Case: O(logN) complexity when there's n site while the bst itself is balance and only 1 route is chosen.

    """

    def __init__(self, sites: list[Land], adventurers: int) -> None:
        """
            Initiallizing a new Bst object and sort the lands according to their guardians to gold ratio.
            Parameters:
                sites: the sites to be stored and sorted in the bst
                adventurers: the number of adventurers to raid all these sites.
            Complexity:
                best case: O(log(N)) where there's only 1 site to be added and theres N sites present in the bst
                worst case: O(Nlog(N)) where there's N sites to be added and every sites needs log(N) steps to be sorted. It constructs the bst from the ground up.
        """
        lands = BinarySearchTree()
        for site in sites:
            lands.__setitem__(site.guardians/site.gold, site)
        self.sites = lands

        self.adventurers = adventurers

    def select_sites(self) -> list[tuple[Land, int]]:
        """
            This method selects the most efficient lands to raid with the initial adventurer number given.
            Returns: a result list which contains tuples of the site and the amount of adventurers sent to this site.
                The result list depends on how many initial adventurers are given to determine how many sites are raided
            Complexity:
                best case: O(log(N)): The bst chooses one route which has a depth of log(N) when theres N nodes in the bst (since the tree is already balanced)
                worst case: O(N): All the guardians add up are still lesser than the amount of raiders, bst goes through all the nodes (N nodes)
        """
        return_list = []
        death_count = 0
        for site in self.sites:
            if self.adventurers >= site.item.guardians:
                return_list.append((site.item, site.item.guardians))
                death_count += site.item.guardians
            else:
                return_list.append((site.item, self.adventurers))
                death_count += self.adventurers
                self.adventurers = death_count
                break
            self.adventurers -= site.item.guardians
        return return_list
            
    def select_sites_from_adventure_numbers(self, adventure_numbers: list[int]) -> list[float]:
        """
            calculates the rewards with different adventurer numbers for every site
            Parameters:
                adventure_numbers: a list of adventure numbers to simulate the amount of gold stolen of every site for every adventurer number.
            Returns:
                result_list: a list which contains the potential amount of gold stolen from every site for every adventurer numbers.
            Complexity:
                best case: O(logN), when theres only 1 adventure number and 1 list to calculate, the bst only chooses 1 route which has a complexity of log(N) when theres N sites.
                worst case: O(N*M), when theres M adventure numbers, the outer for loop runs M times and each time it runs N times for N amount of sites.
        """
        result_list = []
        for adventurer_num in adventure_numbers:
            gold_result = 0
            for site in self.sites:
                if adventurer_num >= site.item.guardians:
                    gold_result += site.item.gold
                else:
                    gold_result += site.item.gold * adventurer_num / site.item.guardians
                    break
                adventurer_num -= site.item.guardians
            result_list.append(gold_result)
        return result_list

    def update_site(self, land: Land, new_reward: float, new_guardians: int) -> None:
        """
            updates the site by deleting the site since there will be no land with the same ratio then set the same site with the updated stats.
            Parameters:
                land: the land to be updated
                new_reward: the new reward of the land
                new_guardians: the new guardians of the land
            Complexity:
                O(log(N)): the __setitem__ and __delitem__ method both have a O(logN) complexity when there's n site while the bst itself is balance.
        """
        self.sites.__delitem__(land.guardians/land.gold)
        land.gold = new_reward
        land.guardians = new_guardians
        self.sites.__setitem__(land.guardians/land.gold, land)