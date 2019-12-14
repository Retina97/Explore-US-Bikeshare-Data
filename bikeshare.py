import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']
def printSecs(seconds):
        m, s = divmod(seconds,60)
        h, m = divmod(m,60)
        d, h = divmod(h,24)
        y, d = divmod(d,365)
        print('Years: {}, Days: {}, Hours: {}, Mins: {}, Secs: {}'.format(y,d,h,m,s))
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nWould you like to see data for Chicago, New York City, or Washington?\n').lower()        
        if city in CITY_DATA:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nWould you like to filter the data by a specefic month, or all?\n').lower()        
        if month in months:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nWould you like to filter the data by a specefic day, or all?\n').title()        
        if day in days:
            break

    print('-'*40)
    return city, month, day


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
    # load data file into a dataframe
    print('Loading from ',CITY_DATA[city])
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int        
        month = months.index(month)+1        
    
        # filter by month to create the new dataframe
        df = df[(df.month == month)]

    # filter by day of week if applicable
    if day != 'All':        
        day = days.index(day)        
        # filter by day of week to create the new dataframe        
        df = df[(df.day_of_week == day)]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Frequent Month:', months[popular_month-1].title())

    # TO DO: display the most common day of week
    popular_dayOfWeek = df['day_of_week'].mode()[0]
    print('Most Frequent Day Of Week:', days[popular_dayOfWeek])

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    hour = df['Start Time'].dt.hour
    popular_hour = hour.mode()[0]
    print('Most Frequent Start Hour:', popular_hour,'H')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_station = df['Start Station'].value_counts().idxmax()
    print('Most Frequent Start Station:', popular_station)
    
    # TO DO: display most commonly used end station
    popular_end = df['End Station'].value_counts().idxmax()
    print('Most Frequent End Station:', popular_end)

    # TO DO: display most frequent combination of start station and end station trip
    #Concat Start station with end station
    Combination_Station = df['Start Station'] + ' => ' + df['End Station']
    popular_comb = Combination_Station.value_counts().idxmax()
    print('Most Frequent Combination:', popular_comb)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel = df['Trip Duration'].sum()
    print('Total Travel Time:')
    printSecs(total_travel)

    # TO DO: display mean travel time
    mean_travel =  df['Trip Duration'].mean()
    print('Mean of Travel Time:', str(datetime.timedelta(seconds=(int)(mean_travel))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print(gender_count)

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print("\nEarliest year of birth: " + str(earliest_birth_year))
        print("\nMost recent year of birth: " + str(most_recent_birth_year))
        print("\nMost common year of birth: " + str(common_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    user_input = input('Do you want to see raw data? Enter yes or no.\n')
    line_number = 0
    while True:
        if user_input.lower() != 'yes':
            break               
        print(df.iloc[line_number : line_number + 5])
        line_number += 5
        user_input = input('\nDo you want to see more raw data? Enter yes or no.\n')         
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)        
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
"""
 i have used StackOverflow and Pandas Official Documentation
 and some of github details
"""