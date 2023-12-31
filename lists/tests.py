from django.test import TestCase

from .models import Item, List


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="Item 1", list=correct_list)
        Item.objects.create(text="Item 2", list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text="Other Item 1", list=other_list)
        Item.objects.create(text="Other Item 2", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, "Item 1")
        self.assertContains(response, "Item 2")

        self.assertNotContains(response, "Other Item 1")
        self.assertNotContains(response, "Other Item 2")

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        _ = List.objects.create()  # create another list

        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        first_item = Item.objects.first()
        self.assertEqual(first_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        new_list = List.objects.first()

        self.assertRedirects(response, f"/lists/{new_list.id}/")


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()
        _ = List.objects.create()  # create another list

        item_text = "A new item for an existing list"
        self.client.post(
            f"/lists/{correct_list.id}/add_item", data={"item_text": item_text}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        correct_list = List.objects.create()
        _ = List.objects.create()  # create another list

        item_text = "A new item for an existing list"
        response = self.client.post(
            f"/lists/{correct_list.id}/add_item", data={"item_text": item_text}
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "First ever item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Second item"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, "First ever item")
        self.assertEqual(saved_items[0].list, list_)
        self.assertEqual(saved_items[1].text, "Second item")
        self.assertEqual(saved_items[1].list, list_)
