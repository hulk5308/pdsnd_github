import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = {1: 'January',
              2: 'February',
              3: 'March',
              4: 'April',
              5: 'May',
              6: 'June',
              7: 'July',
              8: 'August',
              9: 'September',
              10: 'October',
              11: 'November',
              12: 'December'}

DAY_DATA = {0: 'Monday',
              1: 'Tuesday',
              2: 'Wednesday',
              3: 'Thursday',
              4: 'Friday',
              5: 'Saturday',
              6: 'Sunday'}
#refactoring get_filters
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York, or Washington?\n")

    date_filter_type = input("Would you like to filter the data by month, day, both, or not at all? Type \"none\" for no time filte\n")

    if date_filter_type == "month":
        month = input("Which month? (1,2,3,4,5,6,7,8,9,10,11,12)\n")
        day = "none"
    elif date_filter_type == "day":
        month = "none"
        day = input("Which day? Please type your response as an integer (e.g., 0=Monday,1=Tuesday... 6=Sunday)\n")
    elif date_filter_type == "both":
        month = input("Which month? (1,2,3,4,5,6,7,8,9,10,11,12)\n")
        day = input("Which day? Please type your response as an integer (e.g., 1=Monday, 7=Sunday)\n")
    elif date_filter_type == "none":
        month = "none"
        day = "none"

    print('-'*40)
    return city.lower(), month, day

#refactoring load_data
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df_temp = pd.read_csv(CITY_DATA[city])

    #format datetime
    df_temp['Start Time'] = pd.to_datetime(df_temp['Start Time'])
    df_temp['End Time'] = pd.to_datetime(df_temp['End Time'])
    df_temp['month'] = df_temp['Start Time'].dt.month
    df_temp['weekday'] = df_temp['Start Time'].dt.weekday
    df_temp['hour'] = df_temp['Start Time'].dt.hour
    df_temp['start_to_end_station'] = df_temp['Start Station'] + ' --> ' + df_temp['End Station']

    #filter by month and weekday
    if month != "none":
        if day != "none":
            df = df_temp[(df_temp['month'] == int(month)) & (df_temp['weekday'] == int(day))]
        else:
            df = df_temp[(df_temp['month'] == int(month))]
    else:
        if day != "none":
            df = df_temp[(df_temp['weekday'] == int(day))]
        else:
            df = df_temp

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most common month is: " + MONTH_DATA[df['month'].mode()[0]])

    # display the most common day of week
    print("Most common day is: " + df['Start Time'].dt.weekday_name.mode()[0])


    # display the most common start hour
    print("Most common start hour is: " + str(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most common start station is: " + df['Start Station'].mode()[0])

    # display most commonly used end station
    print("Most common end station is: " + df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print("Most common trip is: " + df['start_to_end_station'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time is: " + str(df['Trip Duration'].sum()))

    # display mean travel time
    print("Mean travel time is: " + str(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:")
    print(df['User Type'].value_counts())
    print("")

    if city != 'washington':
        # Display counts of gender
        print("Counts of gender :\n", df['Gender'].value_counts())
        print("")

        # Display earliest, most recent, and most common year of birth
        print("Earliest year of birth: " + str(int(df['Birth Year'].min())))
        print("Most Recent year of birth: " + str(int(df['Birth Year'].max())))
        print("Most common year of birth: " + str(int(df['Birth Year'].mode()[0])))
    else:
        print("There is no \'gender\' and \'birth year\' data for Washington!!!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def print_dataset(city, month, day):
    if month == "none":
        if day == "none":
            print("City: ", city, " Month: none", " Day: none")
        else:
            print("City: ", city, " Month: none", " Day: ", DAY_DATA[int(day)])
    else:
        if day == "none":
            print("City: ", city, " Month: ", MONTH_DATA[int(month)], " Day: none")
        else:
            print("City: ", city, " Month: ", MONTH_DATA[int(month)], " Day: ", DAY_DATA[int(day)])

#refactoring display_data
def display_data(df):
    pd.set_option('display.max_columns', None)# configuration to show all columns
    start_index = 0
    feedback = input("Do you want to see the first 5 rows of data? Enter yes or no.\n")
    while feedback == "yes":
        print('-' * 40)
        print(df.iloc[start_index:(start_index + 5)])
        print('-' * 40)
        start_index += 5
        feedback = input("Do you want to see next 5 rows of data? Enter yes or no.\n")


def main():
    while True:
        city, month, day = get_filters()
        print_dataset(city, month, day)
        df = load_data(city, month, day)
        if df.shape[0] > 0:
            time_stats(df)
            print_dataset(city, month, day)
            station_stats(df)
            print_dataset(city, month, day)
            trip_duration_stats(df)
            print_dataset(city, month, day)
            user_stats(df, city)
            display_data(df)
        else:
            print("\nThere is no data for the current filtering!!!")



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
