from django.test import TestCase

from .models import Item


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_all_list_items(self):
        Item.objects.create(text="Item 1")
        Item.objects.create(text="Item 2")

        response = self.client.get("/lists/the-only-list-in-the-world/")

        self.assertContains(response, "Item 1")
        self.assertContains(response, "Item 2")


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        first_item = Item.objects.first()
        self.assertEqual(first_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})

        self.assertRedirects(response, "/lists/the-only-list-in-the-world/")


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "First ever item"
        first_item.save()

        second_item = Item()
        second_item.text = "Second item"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, "First ever item")
        self.assertEqual(saved_items[1].text, "Second item")
