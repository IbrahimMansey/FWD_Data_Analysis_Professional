import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# months and week lists to use in load_data and stats.
months = ['january', 'february', 'march', 'april', 'may', 'june']
weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'\
            , 'saturday', 'sunday']
    
# general note: if code doesn't run please check load_data function
# if pandas version is 1.0.5 dt.day_name() would work
# if pandas version is old dt.weekday_name will work ok

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
    while True:
        try:
            city = input('choose a city from chicago, new york city or washington: ')
            
            if city.lower().strip() not in CITY_DATA: 
                raise ValueError()
            break
        except ValueError:
            print('value error, try to input a valid city')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('choose a month from january to june or all: ')
            
            # handling all input, whether it was month name or number
            if (month.lower().strip() in months or month.lower().strip() == 'all'\
                or month.lower().strip() in range(1,7)): 
                break
            else: raise ValueError()
        except ValueError:
            print('value error, try to input a valid month or all')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('choose all week or a certain weekday: ')
            
            if (day.lower().strip() in weekdays or day.lower().strip() == 'all'):
                break
            else:  raise ValueError()        
        except ValueError :
            print('value error, try to input a valid day name or all')

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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() # pandas version 1.0.5
    
    # df['day_of_week'] = df['Start Time'].dt.weekday_name for pandas old versions

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
        df['month'] = df['Start Time'].dt.month
        df['month_name'] = df['Start Time'].dt.month_name()
        
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    #check if a month filter was chosen, then no need for most common month stat.
    if len(df['month'].unique()) != 1:
        
        # display the most common month from global months list
        most_common_month = months[df['month'].mode()[0]-1]
    
        print('most common month:', most_common_month)

    #check if a day filter was chosen, then no need for most common day stat.
    if len(df['day_of_week'].unique()) != 1:
        
        # display the most common day of week
        Most_common_weekday = df['day_of_week'].mode()[0]
        
        print('most common day of week:', Most_common_weekday)
    
    # display the most common start hour

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    
    print('Most Popular Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    
    print('most common start station:', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    
    print('most common end station:', most_common_end_station)

    # display most frequent combination of start station and end station trip
    print('most frequent combination is-\nfrom: ' \
          + ('"' + df['Start Station'] + '" to: "' + df['End Station'] \
          + '"').mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('total travel time:', total_travel_time)
    
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('mean travel time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('counts of user types:\n{}\n'.format(df['User Type'].value_counts()))
    
    if city.lower() in ['chicago', 'new york city']: 
        # Display counts of gender
        print('counts of of gender:\n{}\n'.format(df['Gender'].value_counts()))

        # Display earliest, most recent, and most common year of birth
        print('earliest year of birth:', int(df['Birth Year'].min()))
        print('most recent year of birth:', int(df['Birth Year'].max()))
        print('most common year of birth:', int(df['Birth Year'].mode()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """
    Raw data is displayed upon request by the user in this manner:

    function prompt the user if they want to see 5 lines of raw data.
    display that data if the answer is 'yes', and continue these prompts and displays
    until the user says 'no'.
    """
    while True:
        # prompt user whether to view row data.
        display = input('want to see 5 lines preview of the data ?\
                        Enter yes or no.\n ')
        if display.lower() not in ['yes', 'y']:
            break
        else: 
            while True:
                #print first 5 rows
                print(df.head())
                try:
                    # delete first 5 rows to preview next data
                    df = df.iloc[5:]
                    #exception if the data finished and iloc out of range
                except KeyError, IndexError:
                    print('\nthat\'s all of the data filterd')
                    break
                # prompt user to preview more data
                display = input('want to see more of the data ? Enter yes or no.\n ')
                if display.lower() not in ['yes', 'y']:
                    break
            break

def main():
    while True:
        city, month, day = get_filters()
        # check for numeric month input
        if type(month) == int:
            month = months[month-1]
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ['yes', 'y']:
            break


if __name__ == "__main__":
	main()
