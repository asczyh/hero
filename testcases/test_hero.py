from config import settings
from pages import hero_page

class TestHero:

    def test_hero(self, device):
        device.start_app(settings.GAME_PACKAGE, settings.GAME_ACTIVITY)
        heropage = hero_page.HeroPage(device)

        heropage.click_gm()
