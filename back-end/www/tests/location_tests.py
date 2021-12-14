from basic_tests import BasicTest
from models.model_operations import location_operations
from models.model_operations import answer_operations
from models.model_operations import user_operations
from models.model import db
import unittest


class LocationTest(BasicTest):
    """Test case for locations."""

    def setUp(self):
        db.create_all()


    def test_create_location(self):
        """
          Create a location and check if returns a location, and its factory_id as expected. Pass if both.
        """
        FACTORY_ID = "AAAA"

        location = location_operations.create_location(FACTORY_ID)
        #print("create location : " + location.factory_id)
        assert location in db.session
        assert location.factory_id == FACTORY_ID


    def test_remove_location(self):
        """
          Remove the created test case in the previous test. 
          Check if the location first existed in db, then removed successfully. Pass if both.
        """
        FACTORY_ID = "EEEE"

        location = location_operations.create_location(FACTORY_ID)
        assert location in db.session
        location_id = location.id
        location_operations.remove_location(location_id)
        assert location not in db.session


    def test_get_location_by_id(self):
        """
          1. Create a location, get its returned id.
          2. Check if it can be retrieved by the previously returned id. Pass if id is the same.
        """
        FACTORY_ID = "AAAA"

        location = location_operations.create_location(FACTORY_ID)
        location_id = location.id
        retrieved_location = location_operations.get_location_by_id(location_id)
        assert retrieved_location.id == location_id


    def test_get_location_by_factory_id(self):
        """
          1. Create a location with specified factory_id
          2. Get the location with the factory_id. Pass if it exists and the factory_id matches.
        """
        FACTORY_ID = "CCCC"

        location = location_operations.create_location(FACTORY_ID)
        retrieved_location = location_operations.get_location_by_factory_id(FACTORY_ID)
        assert retrieved_location != None
        assert retrieved_location.id == location.id


    def test_set_location_done(self):
        """
          1. Create a location with specified factory_id
          2. Set it done and check the done date. Pass if it's first None then not None after set.
        """
        FACTORY_ID = "CCCC"

        location = location_operations.create_location(FACTORY_ID)
        assert(location.done_at == None)

        location_done = location_operations.set_location_done(location.id, True)
        assert(location_done.done_at != None)


    def test_get_locations(self):
      """
        0. Test no location situation. Pass if assert raises.
        1. Create several Answers which belong to 8 locations, only Loc#2 and Loc#3 have gold answers. Loc#6 never answered by anyone. Loc#7 and Loc#8 has been identified by user u2.
        2. Get locations for user 2, size=5 and gold_standard_size=1 for 5 times. 
        Pass if 5 locations are gotten not including Loc#7 or Loc#8, and only 1 of the 2 locations which have gold answers are gotten.
        3. Test not enough gold standards. Pass if assert raises.
        4. Test not enough location. Pass if assert raises.
      """

      
      u1 = user_operations.create_user("111")
      u2 = user_operations.create_user("222")

      # Test for no location exists.
      with self.assertRaises(Exception) as context:
          locations = location_operations.get_locations(u2.id, 5, 1)

      l1 = location_operations.create_location("AAA")
      l2 = location_operations.create_location("BBB")
      l3 = location_operations.create_location("CCC")
      l4 = location_operations.create_location("DDD")
      l5 = location_operations.create_location("EEE")
      l6 = location_operations.create_location("FFF")
      l7 = location_operations.create_location("GGG")
      l8 = location_operations.create_location("GGG")

      #only l2 and l3 has gold answers. l1, l4, l5, l6 doesn't.
      answer_operations.create_answer(u1.id, l1.id, 2000, 2010, "", 1, 1, False, 0, 0, 0, 0, 0)

      answer_operations.create_answer(u1.id, l2.id, 2000, 2010, "", 1, 1, True, 0, 0, 0, 0, 0)
      answer_operations.create_answer(u1.id, l2.id, 2000, 2010, "", 1, 1, False, 0, 0, 0, 0, 0)
      answer_operations.create_answer(u1.id, l2.id, 2000, 2010, "", 1, 1, False, 0, 0, 0, 0, 0)

      answer_operations.create_answer(u1.id, l3.id, 2000, 2010, "", 1, 1, True, 0, 0, 0, 0, 0)
      answer_operations.create_answer(u1.id, l3.id, 2000, 2010, "", 1, 1, False, 0, 0, 0, 0, 0)
      answer_operations.create_answer(u1.id, l3.id, 2000, 2010, "", 1, 1, False, 0, 0, 0, 0, 0)

      answer_operations.create_answer(u1.id, l4.id, 2000, 2010, "", 1, 1, False, 0, 0, 0, 0, 0)
      answer_operations.create_answer(u1.id, l4.id, 2000, 2010, "", 1, 1, False, 0, 0, 0, 0, 0)
      answer_operations.create_answer(u1.id, l4.id, 2000, 2010, "", 1, 1, False, 0, 0, 0, 0, 0)

      answer_operations.create_answer(u1.id, l5.id, 2000, 2010, "", 1, 1, False, 0, 0, 0, 0, 0)
      answer_operations.create_answer(u1.id, l5.id, 2000, 2010, "", 1, 1, False, 0, 0, 0, 0, 0)
      
      # user answered l7 and l8
      answer_operations.create_answer(u2.id, l7.id, 2000, 2010, "", 1, 1, False, 0, 0, 0, 0, 0)
      answer_operations.create_answer(u2.id, l8.id, 2000, 2010, "", 1, 1, False, 0, 0, 0, 0, 0)


      # Test a common situation.
      for i in range(5):
          locations = location_operations.get_locations(u2.id, 5, 1)

          assert len(locations)==5
          assert not (l2 in locations and l3 in locations)
          assert  l2 in locations or l3 in locations
          assert not (l7 in locations or l8 in locations)

      # Check if exception raises : not enough gold standards
      with self.assertRaises(Exception) as context:
          locations = location_operations.get_locations(u2.id, 5, 3)

      # Check if exception raises : not enough locations
      with self.assertRaises(Exception) as context:
          locations = location_operations.get_locations(u2.id, 7, 3)
      


    def test_get_location_is_done_count(self):
        """
        1. Create 4 locations, mark 3 to be done.
        2. Get the location is done count. Pass if 3.
        """
        l1 = location_operations.create_location("AAA")
        l2 = location_operations.create_location("BBB")
        l3 = location_operations.create_location("CCC")
        l4 = location_operations.create_location("DDD")

        location = location_operations.set_location_done(l1.id, True)
        location = location_operations.set_location_done(l2.id, True)
        location = location_operations.set_location_done(l4.id, True)

        count = location_operations.get_location_is_done_count()
        assert count == 3
    
    
    def test_get_location_count(self):
        """
        1. Create 4 locations
        2. Get the location count. Pass if 4.
        """
        l1 = location_operations.create_location("AAA")
        l2 = location_operations.create_location("BBB")
        l3 = location_operations.create_location("CCC")
        l4 = location_operations.create_location("DDD")
        count = location_operations.get_location_count()
        assert count == 4


if __name__ == "__main__":
    unittest.main()