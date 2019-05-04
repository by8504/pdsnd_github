import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
city_ltrs = {'C': 'Chicago', 'N': 'New York City', 'W': 'Washington'}
month_dict = {'A': 'All', 1: 'January', 2: 'February', 3: "March", 4: 'April',
              5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10:
              'October', 11: 'November', 12: 'December'}
day_dict = {'A': 'All', 'M': 'Monday', 'TU': 'Tuesday', 'W': 'Wednesday',
            'TH': 'Thursday', 'F': 'Friday','SA': 'Saturday', 'SU': 'Sunday'}
day_nums = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
            'Friday': 4, 'Saturday': 5, 'Sunday': 6, 'All': 'A'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('*' * 48)
    print('**Hello! Let\'s explore some US bikeshare data!**')
    print('*' * 48)
    # get user input for city (chicago, new york city, washington).
    choice = 'N'
    while choice == 'N':
        city = ''
        while city == '':
            answer = input('\nWhich city would you like to display data for? '
                           '\n(Type "C" for Chicago, "N" for New York City, '
                           'or "W" for Washington): ').upper()
            if answer in city_ltrs.keys():
                city = city_ltrs[answer].lower()
                print('You chose "{}" for {}'.format(answer, city_ltrs[answer]))
            else:
                print('Invalid City...')
    # get user input for month (all, january, february, ... , june)
        month = ''
        while month == '':
            answer = input('\nPlease select the number of the month to analyze '
                           '\n(Jan: 1, Feb: 2, Mar: 3, etc.) '
                           'or type "A" for all months: ')
            try:
                answer = int(answer)
            except ValueError:
                answer = answer.upper()
            if answer in month_dict.keys():
                month = answer
                print('You chose "{}" for {}'.format(answer, month_dict[answer]))
                if month == 'A':
                    print_month = 'all months'
                else:
                    print_month = month_dict[month]
            else:
                print('Invalid Month...')
    # get user input for day of week (all, monday, tuesday, ... sunday)
        day = ''
        while day == '':
            answer = input('\nPlease select the day of the week to analyze '
                           '\n(M, Tu, W, Th, F, Sa, Su) '
                           'or "A" for all days: ').upper()
            if answer in day_dict.keys():
                day = day_dict[answer]
                print('You chose "{}" for {}'.format(answer, day_dict[answer]))
                if day == 'All':
                    print_day = 'all day'
                else:
                    print_day = day
            else:
                print('Invalid Day...')
        choice = ''
        while choice == '':
            answer = input(
                '\nDo you wish to analyze data for the city of {} for {}s in '
                '{}? \n(Type "Y" to proceed or "N" to start '
                'over): '.format(city.title(), print_day, print_month)).upper()
            if answer == 'Y':
                choice = answer
                print('-' * 40)
            elif answer == 'N':
                choice = answer
            else:
                choice = ''
                print('Not a valid response...')

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
    # convert values to filter:

    day = day_nums[day]
    df = pd.read_csv(CITY_DATA[city])
    if df['Start Time'].isnull().sum() != 0:
        df.dropna(axis=0)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Weekday'] = df['Start Time'].dt.dayofweek
    df['Month'] = df['Start Time'].dt.month
    df['Hour'] = df['Start Time'].dt.hour

    # Check whether or not values exist in data

    df_check = df.groupby(['Month']).count()
    df_check = df_check.index.values
    if month != 'A':
        if month not in df_check:
            print('Sorry, there is no data for the month of {} in the city of '
                  '{}. Data only exists for the following '
                  'months:'.format(month_dict[month], city.title()))
            for x in df_check:
                print(month_dict[df_check[x-1]])

    # Filter

    if month != 'A':
        df = df[df['Month'] == month]
    if day != 'A':
        df = df[df['Weekday'] == day]

    return df


def raw_data(df, city):
    """Prompts user to see raw data from the filtered dataframe"""
    rd_answer = 'y'
    x = 0
    while rd_answer == 'y':
        if x == 0:
            rd_answer = input('Would you like to see raw data from the '
                              'specified period for {}? \n("Y" to review data'
                              ' or "N" to skip): '.format(city.title())).lower()
        else:
            rd_answer = input('\nWould you like to see the next 5 lines of raw '
                              'data?\n ("Y" to continue or "N" to skip)')
        if rd_answer == 'y':
            print(df.iloc[x:x + 5])
            x += 5
        elif rd_answer != 'y' and rd_answer != 'n':
            print('Please select a valid response ("Y" or "N").')
            rd_answer = 'y'


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    day_str = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
               4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    hour_mode = int(df['Hour'].mode()[0])
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month != 'A':
        print('All data are from the month of '
              '{}'.format(month_dict[month].title()))
    else:
        month_mode = int(df['Month'].mode())
        print('The most common month for rentals '
              'is {}'.format(month_dict[month_mode].title()))

    # display the most common day of week
    if day != 'All':
        print('All data are for {}s'.format(day.title()))
    else:
        day_mode = int(df['Weekday'].mode())
        print('The most common day for rentals is {}'.format(day_str[day_mode]))

    # display the most common start hour
    hour_dict = {0: '12:00 AM', 1: '1:00 AM', 2: '2:00 AM', 3: '3:00 AM',
                 4: '4:00 AM', 5: '5:00 AM', 6: '6:00 AM', 7: '7:00 AM',
                 8: '8:00 AM', 9: '9:00 AM', 10: '10:00 AM', 11: '11:00 AM',
                 12: '12:00 PM', 13: '1:00 PM', 14: '2:00 PM', 15: '3:00 PM',
                 16: '4:00 PM', 17: '5:00 PM', 18: '6:00 PM',19: '7:00 PM',
                 20: '8:00 PM', 21: '9:00 PM', 22: '10:00 PM', 23: '11:00 PM'}
    if hour_mode < 23:
        hour_end = hour_mode + 1
    else:
        hour_end = 0
    print('The most common hour for rentals is between {} '
          'and {}'.format(hour_dict[hour_mode], hour_dict[hour_end]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trips...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_mode = df['Start Station'].mode().iloc[0]
    print('The most commonly used start station is '
          '{}'.format(start_station_mode))

    # display most commonly used end station
    end_station_mode = df['End Station'].mode().iloc[0]
    print('The most commonly used end station is {}'.format(end_station_mode))

    # display most frequent combination of start station and end station trip
    combo_df = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    combo = combo_df.index.values[0]
    start = combo[0]
    end = combo[1]
    print('\nThe most common trips start at the {} station \nand end at the '
          '{} station.'.format(start, end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['duration'] = df['End Time'] - df['Start Time']
    total_time = df['duration'].sum()
    print('The total time traveled in {} for this period is '
          '{}.'.format(city.title(), total_time))

    # display mean travel time
    mean_time = df['duration'].mean()
    print('The average time traveled in {} for this period is '
          '{}.'.format(city.title(), mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types = df.groupby(['User Type']).count()
    user_types = user_types.index.values
    for ut in user_types:
        user_df = df[df['User Type'] == ut]
        print('The number of users who are {}s in {} is '
              '{}.'.format(ut.lower(),
                           city.title(),
                           user_df['Start Time'].count()))
    print('\n')

    # Display counts of gender
    try:
        user_gender = df.groupby(['Gender']).count()
        user_gender = user_gender.index.values
        for ug in user_gender:
            user_df = df[df['Gender'] == ug]
            print('The number of users in {} who are {} is '
                  '{}.'.format(city.title(),
                               ug.lower(),
                               user_df['Start Time'].count()))
    except (KeyError, NameError):
        print('There are no gender statistics for the city of '
              '{}.'.format(city.title()))
    # Display earliest, most recent, and most common year of birth
    try:
        birth_year_min = int(df['Birth Year'].min())
        birth_year_max = int(df['Birth Year'].max())
        birth_year_mode = df['Birth Year'].mode()
        birth_year_mode = int(birth_year_mode[0])
        print('\nThe earliest birth year for users in {} is '
              '{}.'.format(city.title(), birth_year_min))
        print('The most recent birth year for users in {} is '
              '{}.'.format(city.title(), birth_year_max))
        print('The most common birth year for user in {} is '
              '{}'.format(city.title(), birth_year_mode))
    except KeyError:
        print('\nThere are no birth year statistics for the city of '
              '{}.'.format(city.title()))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        raw_data(df, city)
        try:
            time_stats(df, month, day)
            station_stats(df)
            trip_duration_stats(df, city)
            user_stats(df, city)
        except (IndexError, TypeError):
            print('Please select a valid Month/Day combination.')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
