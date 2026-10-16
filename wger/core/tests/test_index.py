# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

# Django
from django.conf import settings
from django.test import SimpleTestCase
from django.urls import reverse

# wger
from wger.core.templatetags.wger_extras import mobile_tab
from wger.core.tests.base_testcase import WgerTestCase


class IndexTestCase(WgerTestCase):
    """
    Tests the index page and the mobile app shell
    """

    def wger_settings(self, **kwargs):
        return {**settings.WGER_SETTINGS, **kwargs}

    def test_anonymous_sees_welcome_screen(self):
        response = self.client.get(reverse('core:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'welcome.html')
        self.assertContains(response, reverse('core:user:login'))
        self.assertContains(response, reverse('core:user:registration'))
        self.assertContains(response, reverse('core:user:demo-entries'))
        self.assertContains(response, reverse('software:features'))

    def test_welcome_screen_respects_settings(self):
        with self.settings(
            WGER_SETTINGS=self.wger_settings(ALLOW_REGISTRATION=False, ALLOW_GUEST_USERS=False)
        ):
            response = self.client.get(reverse('core:index'))

        self.assertContains(response, reverse('core:user:login'))
        self.assertNotContains(response, reverse('core:user:registration'))
        self.assertNotContains(response, reverse('core:user:demo-entries'))

    def test_logged_in_redirects_to_dashboard(self):
        self.user_login('test')
        response = self.client.get(reverse('core:index'))

        self.assertRedirects(response, reverse('core:dashboard'), fetch_redirect_response=False)

    def test_tab_bar_for_logged_in_users(self):
        self.user_login('test')
        response = self.client.get(reverse('core:dashboard'))

        self.assertContains(response, 'app-tabbar')
        self.assertContains(response, 'id="app-more"')
        # Regular users don't get the administration links
        self.assertNotContains(response, reverse('core:language:overview'))

    def test_no_tab_bar_for_anonymous_users(self):
        response = self.client.get(reverse('exercise:exercise:overview'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'app-tabbar')

    def test_admin_links_in_navbar_and_more_sheet(self):
        self.user_login('admin')
        response = self.client.get(reverse('core:dashboard'))

        self.assertContains(response, reverse('core:language:overview'), count=2)


class MobileTabTestCase(SimpleTestCase):
    """
    Tests the mapping of URL paths to tabs of the mobile bottom bar
    """

    def test_mobile_tab(self):
        self.assertEqual(mobile_tab('/en/dashboard'), 'home')
        self.assertEqual(mobile_tab('/de/routine/5/view'), 'workouts')
        self.assertEqual(mobile_tab('/en/nutrition/overview/'), 'food')
        self.assertEqual(mobile_tab('/en/weight/overview'), 'progress')
        self.assertEqual(mobile_tab('/en/measurement/'), 'progress')
        self.assertEqual(mobile_tab('/en/gallery/images/overview'), 'progress')
        self.assertEqual(mobile_tab('/en/gym/1/user-list'), '')
        self.assertEqual(mobile_tab('/en/'), '')
        self.assertEqual(mobile_tab('/'), '')
