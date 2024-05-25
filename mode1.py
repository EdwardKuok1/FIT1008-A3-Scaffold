from landsites import Land
from data_structures.bst import BinarySearchTree

class Mode1Navigator:
    """
    Student-TODO: short paragraph as per
    https://edstem.org/au/courses/14293/lessons/46720/slides/318306
    """

    def __init__(self, sites: list[Land], adventurers: int) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        lands = BinarySearchTree()
        for site in sites:
            lands.__setitem__(site.guardians/site.gold, site)
        self.sites = lands

        self.adventurers = adventurers

    def select_sites(self) -> list[tuple[Land, int]]:
        """
        Student-TODO: Best/Worst Case
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
        Student-TODO: Best/Worst Case
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
        Student-TODO: Best/Worst Case
        """
        self.sites.__delitem__(land.guardians/land.gold)
        land.gold = new_reward
        land.guardians = new_guardians
        self.sites.__setitem__(land.guardians/land.gold, land)