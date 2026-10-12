from pages import hero_page

class TestHero:

    def test_hero(self,driver):
        heropage = hero_page.HeroPage(driver)

        heropage.click_gm()
