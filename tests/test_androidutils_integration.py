from collections import OrderedDict

import pytest

from locawise.androidutils import parse_xml_file, serialize_to_xml
from locawise.errors import MalformedAndroidStringsXMLError
from tests.utils import get_absolute_path

_XML_DECLARATION = '<?xml version=\'1.0\' encoding=\'utf-8\'?>'


@pytest.mark.asyncio(loop_scope="module")
async def test_parse_xml_file_invalid_tree():
    test_file = get_absolute_path("resources/androidxml/invalid.xml")

    with pytest.raises(MalformedAndroidStringsXMLError):
        await parse_xml_file(test_file)


# should return empty string when resource has no children
@pytest.mark.asyncio(loop_scope="module")
async def test_parse_xml_file_tree_with_no_children():
    test_file = get_absolute_path("resources/androidxml/no_children.xml")

    actual = await parse_xml_file(test_file)

    assert actual == {}


# should return correct output when resource has only strings
@pytest.mark.asyncio(loop_scope="module")
async def test_parse_xml_file_tree_with_only_string_children():
    test_file = get_absolute_path("resources/androidxml/only_strings.xml")

    actual = await parse_xml_file(test_file)

    expected = OrderedDict()
    expected['app_name'] = 'Travel Buddy'
    expected['welcome_message'] = 'Welcome to Travel Buddy!'
    expected['login_prompt'] = 'Please log in to continue'
    expected['email_hint'] = 'Email address'
    expected['password_hint'] = 'Password'
    expected['forgot_password'] = 'Forgot password?'
    expected['login_button'] = 'Log In'
    expected['signup_prompt'] = "Don\\'t have an account? Sign up now"
    expected['greeting'] = 'Hello, %1$s!'
    expected['last_login'] = 'Your &amp;last login was on %1$s at %2$s'
    expected['temperature'] = 'Current temperature: %1$d°C'
    expected['terms_conditions'] = 'By continuing, you agree to our <b>Terms of Service</b> and <i>Privacy Policy</i>'
    expected['search_query_example'] = 'Try searching for \\"popular destinations\\"'

    assert actual == expected


# should return correct output when resource has only string arrays
@pytest.mark.asyncio(loop_scope="module")
async def test_parse_xml_file_tree_with_only_string_array_children():
    test_file = get_absolute_path("resources/androidxml/only_string_arrays.xml")

    actual = await parse_xml_file(test_file)

    expected = OrderedDict()
    expected["travel_categories_/_0"] = "Beach Vacations"
    expected["travel_categories_/_1"] = "Mountain Retreats"
    expected["travel_categories_/_2"] = "City Escapes"
    expected["travel_categories_/_3"] = "Cultural Tours"
    expected["travel_categories_/_4"] = "Adventure Trips"
    expected["travel_categories_/_5"] = "Culinary Journeys"
    expected["transport_modes_/_0"] = "Flight"
    expected["transport_modes_/_1"] = "Train"
    expected["transport_modes_/_2"] = "Bus"
    expected["transport_modes_/_3"] = "Car"
    expected["transport_modes_/_4"] = "Cruise"
    expected["transport_modes_/_5"] = "Walking Tour"
    expected["currency_codes_/_0"] = "USD"
    expected["currency_codes_/_1"] = "EUR"
    expected["currency_codes_/_2"] = "GBP"
    expected["currency_codes_/_3"] = "JPY"
    expected["currency_codes_/_4"] = "AUD"
    expected["currency_codes_/_5"] = "CAD"

    assert actual == expected


# should return correct output when resource has only plurals
@pytest.mark.asyncio(loop_scope="module")
async def test_parse_xml_file_tree_with_only_plurals_children():
    test_file = get_absolute_path("resources/androidxml/only_plurals.xml")

    actual = await parse_xml_file(test_file)

    expected = OrderedDict()
    expected["notifications_count___zero"] = "No new notifications"
    expected["notifications_count___one"] = "You have 1 new notification"
    expected["notifications_count___other"] = "You have %d new notifications"
    expected["trip_days_remaining___zero"] = "Your trip starts today!"
    expected["trip_days_remaining___one"] = "1 day until your trip"
    expected["trip_days_remaining___other"] = "%d days until your trip"
    expected["photos_saved___one"] = "1 photo saved to your collection"
    expected["photos_saved___other"] = "%d photos saved to your collection"
    expected["destination_visits___zero"] = "You haven't visited %s yet"
    expected["destination_visits___one"] = "You've visited %s once"
    expected["destination_visits___other"] = "You've visited %s %d times"

    assert actual == expected


# should return correct output when resource has mixed
@pytest.mark.asyncio(loop_scope="module")
async def test_parse_xml_file_tree_with_mixed_children():
    test_file = get_absolute_path("resources/androidxml/mixed.xml")

    actual = await parse_xml_file(test_file)

    expected = OrderedDict()
    expected['app_name'] = 'Travel Buddy Pro'
    expected['welcome_message'] = 'Welcome to Travel Buddy Pro!'
    expected['app_version'] = 'Version 2.5.1'
    expected['login_prompt'] = 'Please log in to continue'
    expected['email_hint'] = 'Email address'
    expected['password_hint'] = 'Password'
    expected['forgot_password'] = 'Forgot password?'
    expected['login_button'] = 'Log In'
    expected['signup_prompt'] = "Don\\'t have an account? Sign up now"
    expected['logout'] = 'Log Out'
    expected['settings'] = 'Settings'
    expected['help'] = 'Help &amp; Support'
    expected['app_description'] = 'Travel Buddy Pro:\\nYour ultimate companion\\nfor seamless travel experiences'
    expected['welcome_paragraph'] = ('Welcome to Travel Buddy Pro!\\n\\nWe\\\'re excited to help you plan your next '
                                     'adventure.\\nDiscover amazing destinations and create memories that last a '
                                     'lifetime.')
    expected['multi_paragraph'] = (
        'Planning your trip has never been easier.\\n\\nWith our advanced tools, you can:\\n- '
        'Find the best deals\\n- Discover hidden gems\\n- Connect with fellow travelers\\n\\nStart '
        'your journey today!')
    expected['greeting'] = 'Hello, %1$s!'
    expected['last_login'] = 'Your last login was on %1$s at %2$s'
    expected['temperature'] = 'Current temperature: %1$d°C'
    expected['weather_forecast'] = 'Today: %1$s, Tomorrow: %2$s'
    expected['trip_summary'] = 'Your %1$s trip to %2$s includes %3$d activities'
    expected['budget_info'] = 'Budget: %1$.2f %2$s - Spent: %3$.2f %2$s'
    expected['complex_format'] = 'Trip #%1$d: %2$s to %3$s (%4$s - %5$s) - %6$.2f %7$s'
    expected['percentage_complete'] = 'Your itinerary is %1$d%% complete'
    expected['terms_conditions'] = 'By continuing, you agree to our <b>Terms of Service</b> and <i>Privacy Policy</i>'
    expected['premium_features'] = 'Unlock <font color="#FFD700">premium features</font> for enhanced travel planning'
    expected['safety_warning'] = (
        '<font color="#FF0000">Important:</font> Always check <b>travel advisories</b> before '
        'booking')
    expected[
        'html_mix'] = ('<b>Bold text</b> with <i>italic</i> and <u>underlined</u> parts mixed with <font '
                       'color="#00FF00">colored text</font> in a single string')
    expected['nested_html'] = '<b>Bold text with <i>italic inside bold</i> and more bold</b> followed by regular text'
    expected['empty_string'] = ''
    expected[
        'terms_full'] = ('This Travel Buddy Pro End User License Agreement (\\"Agreement\\") is a legal document '
                         'between'
                         ' you and Travel Buddy Pro, Inc. By downloading, installing, or using this application, '
                         'you agree to be bound by the terms of this Agreement. This application is licensed, '
                         'not sold, to you for use strictly in accordance with the terms and conditions of this '
                         'Agreement. Travel Buddy Pro reserves all rights not expressly granted to you. This is a '
                         'very long string that continues with many more details about terms and conditions that need '
                         'to be displayed in the application and properly handled by any parser that might be '
                         'processing this strings.xml file. The parser should handle strings of arbitrary length '
                         'without truncation or memory issues.')
    expected["travel_categories_/_0"] = "Beach Vacations"
    expected["travel_categories_/_1"] = "Mountain Retreats"
    expected["travel_categories_/_2"] = "City Escapes"
    expected["travel_categories_/_3"] = "Cultural Tours"
    expected["travel_categories_/_4"] = "Adventure Trips"
    expected["travel_categories_/_5"] = "Culinary Journeys"
    expected["travel_categories_/_6"] = "Wildlife Safaris"
    expected["travel_categories_/_7"] = "Historical Expeditions"
    expected["travel_categories_/_8"] = "Wellness &amp; Spa Retreats"
    expected["travel_categories_/_9"] = "Eco-Tourism"
    expected["transport_modes_/_0"] = "Flight"
    expected["transport_modes_/_1"] = "Train"
    expected["transport_modes_/_2"] = "Bus"
    expected["transport_modes_/_3"] = "Car"
    expected["transport_modes_/_4"] = "Cruise"
    expected["transport_modes_/_5"] = "Walking Tour"
    expected["transport_modes_/_6"] = "Bicycle"
    expected["transport_modes_/_7"] = "Motorcycle"
    expected["transport_modes_/_8"] = "Ferry"
    expected["transport_modes_/_9"] = "Helicopter"
    expected["travel_tips_/_0"] = "Always keep digital copies of important documents"
    expected["travel_tips_/_1"] = "Learn a few phrases in the local language"
    expected["travel_tips_/_2"] = "Notify your bank about your travel dates"
    expected["travel_tips_/_3"] = "Pack a basic first aid kit"
    expected["travel_tips_/_4"] = "Research local customs &amp; etiquette"
    expected["travel_tips_/_5"] = "Check if you need travel insurance"
    expected["travel_tips_/_6"] = "Download offline maps of your destination"
    expected["travel_tips_/_7"] = "Keep emergency contacts handy"
    expected["travel_tips_/_8"] = "Pack a universal power adapter"
    expected["travel_tips_/_9"] = "Take photos of your luggage contents"
    expected["multiline_items_/_0"] = "First line\\nSecond line"
    expected["multiline_items_/_1"] = "Item with\\nmultiple\\nnewlines"
    expected["multiline_items_/_2"] = "Another\\nexample"
    expected["notifications_count___zero"] = "No new notifications"
    expected["notifications_count___one"] = "You have 1 new notification"
    expected["notifications_count___other"] = "You have %d new notifications"
    expected["trip_days_remaining___zero"] = "Your trip starts today!"
    expected["trip_days_remaining___one"] = "1 day until your trip"
    expected["trip_days_remaining___other"] = "%d days until your trip"
    expected["places_nearby___zero"] = "No interesting places nearby"
    expected["places_nearby___one"] = "1 interesting place within %d meter"
    expected["places_nearby___other"] = "%1$d interesting places within %2$d meters"
    expected["reviews_count___zero"] = "No reviews yet. Be the first!"
    expected["reviews_count___one"] = "%1$d review (%2$.1f stars)"
    expected["reviews_count___other"] = "%1$d reviews (%2$.1f stars)"
    expected["bullet_point"] = '•'
    expected["copyright_notice"] = '© 2025 Travel Buddy Pro, Inc.'
    expected["trademark"] = 'Travel Buddy Pro™ - All rights reserved'
    expected["registered"] = 'Travel Buddy® is a registered trademark'
    expected["degree_symbol"] = 'Current: 23°C | Feels like: 25°C'
    expected["currency_symbols"] = 'Accepted: $ € £ ¥'
    expected["math_symbols"] = 'Distance: d = √((x₂-x₁)² + (y₂-y₁)²)'
    expected["emoji_example"] = '✈️ 🏨 🏖️ 🗺️ 🌍 🧳'

    assert actual == expected


# should return empty resources when pairs are empty
def test_serialize_to_xml_empty_pairs():
    pairs = {}

    actual = serialize_to_xml(pairs)

    expected = f"""{_XML_DECLARATION}
<resources />"""
    assert actual == expected


# should return correct output when only string pairs exist
def test_serialize_to_xml_only_string_pairs():
    pairs = {
        'main_title': 'Travel Buddy',
        'welcome_message': 'Welcome to Travel Buddy!',
        'app_version': 'Version 1.0.0',
        'login_prompt': 'Please log in to continue',
        'email_hint': 'Email address',
        'password_hint': 'Password',
        'forgot_password': 'Forgot password?',
    }

    actual = serialize_to_xml(pairs)

    expected = f"""{_XML_DECLARATION}
<resources>
    <string name="main_title">Travel Buddy</string>
    <string name="welcome_message">Welcome to Travel Buddy!</string>
    <string name="app_version">Version 1.0.0</string>
    <string name="login_prompt">Please log in to continue</string>
    <string name="email_hint">Email address</string>
    <string name="password_hint">Password</string>
    <string name="forgot_password">Forgot password?</string>
</resources>"""
    assert actual == expected


# should return correct output when only plurals exist
def test_serialize_to_xml_only_plurals():
    pairs = {
        'notifications_count___zero': 'No new notifications',
        'notifications_count___one': 'You have 1 new notification',
        'notifications_count___other': 'You have %d new notifications',
        'trip_days_remaining___zero': 'Your trip starts today!',
        'trip_days_remaining___one': '1 day until your trip',
        'trip_days_remaining___other': '%d days until your trip',
    }

    actual = serialize_to_xml(pairs)

    expected = f"""{_XML_DECLARATION}
<resources>
    <plurals name="notifications_count">
        <item quantity="zero">No new notifications</item>
        <item quantity="one">You have 1 new notification</item>
        <item quantity="other">You have %d new notifications</item>
    </plurals>
    <plurals name="trip_days_remaining">
        <item quantity="zero">Your trip starts today!</item>
        <item quantity="one">1 day until your trip</item>
        <item quantity="other">%d days until your trip</item>
    </plurals>
</resources>"""
    assert actual == expected


# should return correct output when only string arrays exist
def test_serialize_to_xml_only_string_arrays():
    pairs = {
        'travel_categories_/_0': 'Beach Vacations',
        'travel_categories_/_1': 'Mountain Retreats',
        'travel_categories_/_2': 'City Escapes',
        'travel_categories_/_3': 'Cultural Tours',
        'travel_categories_/_4': 'Adventure Trips',
        'travel_categories_/_5': 'Culinary Journeys',
        'transport_modes_/_0': 'Flight',
        'transport_modes_/_1': 'Train',
        'transport_modes_/_2': 'Bus',
    }

    actual = serialize_to_xml(pairs)

    expected = f"""{_XML_DECLARATION}
<resources>
    <string-array name="travel_categories">
        <item>Beach Vacations</item>
        <item>Mountain Retreats</item>
        <item>City Escapes</item>
        <item>Cultural Tours</item>
        <item>Adventure Trips</item>
        <item>Culinary Journeys</item>
    </string-array>
    <string-array name="transport_modes">
        <item>Flight</item>
        <item>Train</item>
        <item>Bus</item>
    </string-array>
</resources>"""

    assert actual == expected


# should return correct output when mixed
def test_serialize_to_xml_mixed():
    pairs = {
        'app_name': 'Travel Buddy Pro',
        'welcome_message': 'Welcome to Travel Buddy Pro!',
        'app_version': 'Version 2.5.1',
        'login_prompt': 'Please log in to continue',
        'email_hint': 'Email address',
        'forgot_password': 'Forgot password?',
        'login_button': 'Log In',
        'signup_prompt': "Don\\'t have an account? Sign up now",
        'notifications_count___zero': 'No new notifications',
        'notifications_count___one': 'You have 1 new notification',
        'notifications_count___other': 'You have %d new notifications',
        'cities_/_0': 'New York',
        'cities_/_1': 'Los Angeles',
        'cities_/_2': 'Chicago',
        'logout': 'Log Out',
        'settings': 'Settings',
        'visited_destinations_/_0': 'Paris',
        'visited_destinations_/_1': 'Tokyo',
        'visited_destinations_/_2': 'London',
        'missing_person_count___zero': 'No missing persons',
        'missing_person_count___one': '1 missing person',
        'missing_person_count___other': '%d missing persons',
        'contact_support': 'Contact Support',
        'free_trial': 'Start Free Trial'
    }

    actual = serialize_to_xml(pairs)

    expected = f"""{_XML_DECLARATION}
<resources>
    <string name="app_name">Travel Buddy Pro</string>
    <string name="welcome_message">Welcome to Travel Buddy Pro!</string>
    <string name="app_version">Version 2.5.1</string>
    <string name="login_prompt">Please log in to continue</string>
    <string name="email_hint">Email address</string>
    <string name="forgot_password">Forgot password?</string>
    <string name="login_button">Log In</string>
    <string name="signup_prompt">Don\\'t have an account? Sign up now</string>
    <plurals name="notifications_count">
        <item quantity="zero">No new notifications</item>
        <item quantity="one">You have 1 new notification</item>
        <item quantity="other">You have %d new notifications</item>
    </plurals>
    <string-array name="cities">
        <item>New York</item>
        <item>Los Angeles</item>
        <item>Chicago</item>
    </string-array>
    <string name="logout">Log Out</string>
    <string name="settings">Settings</string>
    <string-array name="visited_destinations">
        <item>Paris</item>
        <item>Tokyo</item>
        <item>London</item>
    </string-array>
    <plurals name="missing_person_count">
        <item quantity="zero">No missing persons</item>
        <item quantity="one">1 missing person</item>
        <item quantity="other">%d missing persons</item>
    </plurals>
    <string name="contact_support">Contact Support</string>
    <string name="free_trial">Start Free Trial</string>
</resources>"""
    assert actual == expected
