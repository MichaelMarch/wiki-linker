# Wiki Linker

A python bot for finding a path (of articles) between 2 wikipedia articles.

Note: **Currrently the project can only list links of the supplied articles.**

## Usage

### Prerequisites and Installing
To try this project you should have the modules that are listed in [requirements.txt](requirements.txt) installed. The best way to do it is to create a virtual environment:

```
python -m venv .venv
```

and then enter the virtual environment:

```
# for Windows (powershell)
.\.venv\Scripts\activate

# or for UNIX systems
source .venv\Scripts\activate.sh
```

Finally you can install the required modules by:

```
pip install -r requirements.txt
```

### Running the project

```
python wiki_linker.py article_A article_B
```

For example if you run:
```
python wiki_linker.py William_L._Webber 12_Downing_Street
```

The output should be (as of 06-14-2022):
<details> 
  <summary>The output (click the arrow on the left to see it)</summary>
    Article A:<br>
    Michigan_Senate<br>
    Michigan%27s_25th_Senate_district<br>
    Wesley_P._Andrus<br>
    List_of_mayors_of_Saginaw,_Michigan<br>
    Ogden,_New_York<br>
    Democratic_Party_(United_States)<br>
    Michigan<br>
    Saginaw_County,_Michigan<br>
    Democratic_National_Convention<br>
    1876_Michigan_gubernatorial_election<br>
    Charles_Croswell<br>
    Odd_Fellows<br>
    Knights_Templar<br>
    Saginaw,_Michigan<br>
    Find_a_Grave<br>
    Library_of_Michigan<br>
    Henry_Chamberlain_(Michigan_politician)<br>
    Governor_of_Michigan<br>
    Orlando_M._Barnes<br><br>
    Article B:<br>
    Downing_Street<br>
    City_of_Westminster<br>
    Chief_Whip<br>
    Prime_Minister_of_the_United_Kingdom<br>
    Judge_Advocate_General_of_the_Armed_Forces<br>
    Colonial_Office<br>
    10_Downing_Street<br>
    11_Downing_Street<br>
    9_Downing_Street<br>
    Stucco<br>
    Charles_Barry<br>
    Cabinet_Office<br>
    Whitehall<br>
    East_India_Company<br>
    Herbert_Gladstone,_1st_Viscount_Gladstone<br>
    Chancellor_of_the_Exchequer<br>
    William_Ewart_Gladstone<br>
    Home_Secretary<br>
    Recruitment_to_the_British_Army_during_the_First_World_War<br>
    Asquith_coalition_ministry<br>
    Liberal_Party_(UK)<br>
    John_Gulland<br>
    Alastair_Campbell<br>
    Tony_Blair<br>
    Privy_Council_of_the_United_Kingdom<br>
    Gordon_Brown<br>
    Evening_Standard<br>
    British_History_Online<br>
    Life_(magazine)<br>
    British_Newspaper_Archive<br>
    Yorkshire_Evening_Post<br>
    The_Daily_Telegraph<br>
    Privy_Council_Office_(United_Kingdom)<br>
    First_Lord_of_the_Treasury<br>
    Parliamentary_Secretary_to_the_Treasury<br>
    Chief_Mouser_to_the_Cabinet_Office<br>
    Principal_Private_Secretary_to_the_Prime_Minister_of_the_United_Kingdom<br>
    Parliamentary_Private_Secretary_to_the_Prime_Minister<br>
    Political_Secretary_to_the_Prime_Minister_of_the_United_Kingdom<br>
    Downing_Street_Chief_of_Staff<br>
    Downing_Street_Director_of_Communications<br>
    Downing_Street_Press_Secretary<br>
    Number_10_Policy_Unit<br>
    Downing_Street_Press_Briefing_Room<br>
    Partygate<br>
    Geographic_coordinate_system<br>
</details>  

## Development

The project was created and tested only on Windows. Don't know if the project runs on other platform. I am 90% sure it should hae run faster on UNIX.

Any contribution is welcome :)

## License

This project is unlicensed - please refer to [LICENSE](LICENSE) file for more details.

