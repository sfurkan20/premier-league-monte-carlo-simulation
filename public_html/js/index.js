class Team {
    name;
    played;
    won;
    drawn;
    goalsFor;
    goalsAgainst;
    strength;

    constructor(name, strength) {
        this.name = name;
        this.strength = strength;
        this.played = 0;
        this.won = 0;
        this.drawn = 0;
        this.goalsFor = 0;
        this.goalsAgainst = 0;
    }

    get lost() {
        return this.played - this.won - this.drawn;
    }

    get goalDifference() {
        return this.goalsFor - this.goalsAgainst;
    }

    get points() {
        return (3 * this.won) + this.drawn;
    }

    get championshipChance() {
        if (teamsDataForWeeks[teamsDataForWeeks.length - 1] === undefined) {
            return NaN;
        }

        let totalWinsInLeague = 0;
        let totalDrawsInLeague = 0;
        teamsDataForWeeks[teamsDataForWeeks.length - 1].forEach((element)=>{
            totalWinsInLeague += element.won;
            totalDrawsInLeague += element.drawn;
        });
        totalDrawsInLeague /= 2;

        return (this.won * 3 + this.drawn) / (totalWinsInLeague * 3 + totalDrawsInLeague * 2);
    }
}

var teams = []
var teamsDataForWeeks = [];
var matchRecordsForWeeks = []
var fixture = []

let currentWeek = 1;

function constructLeagueTableRowHTML(position, team) {
    return `<tr class="zone">
    <td><span>${position}</span></td>
    <td>${team.name}</td>
    <td><span>${team.played}</span></td>
    <td><span>${team.won}</span></td>
    <td><span>${team.drawn}</span></td>
    <td><span>${team.lost}</span></td>
    <td><span>${team.goalsFor}</span></td>
    <td><span>${team.goalsAgainst}</span></td>
    <td><span class=${team.goalDifference > 0 ? "positive" : team.goalDifference < 0 ? "negative" : ""}>${team.goalDifference}</span></td>
    <td><span>${team.points}</span></td>
    <td><span>${team.strength}</span></td>
    <td><span>${isNaN(team.championshipChance) ? "Unknown" : team.championshipChance}</span></td>
    </tr>`
}

fetch('/get_teams').then((response => response.json()))
    .then(data => {
        for (let i = 0; i < data.length; i++) {
            const team = new Team(data[i].name, data[i].strength);
            teams.push(team);

            document.getElementById("table-body").innerHTML += constructLeagueTableRowHTML(i + 1, team);
        }

        fixture = generateFixture(38);
    });

function generateFixture(weekCount) {
    let fixture = []
    let reversed = false;
    for (let i = 1; i <= weekCount; i++) {
        if (i % 2 == 0) {
            if (reversed) {
                fixture.push([[teams[0], teams[3]], [teams[1], teams[2]]])
            } else {
                fixture.push([[teams[3], teams[0]], [teams[2], teams[1]]])
            }
            reversed = !reversed;
        } else {
            if (reversed) {
                fixture.push([[teams[1], teams[3]], [teams[0], teams[2]]])
            } else {
                fixture.push([[teams[3], teams[1]], [teams[2], teams[0]]])
            }
        }
    }

    return fixture;
}

function constructMatchResultHTML(team1Name, team1Goal, team2Name, team2Goal) {
    return `<tr>
        <td>
            <h2>${team1Name} </h2>
        </td>
        <td>
            <input type="number" class="fixMatch-input" style="width: 30px" value="${team1Goal}"></input>
        </td>
        <td>
            <h2> - </h2>
        </td>
        <td>
            <input type="number" class="fixMatch-input" style="width: 30px" value="${team2Goal}"></input>
        </td>
        <td>
            <h2> ${team2Name}</h2>
        </td>
    </tr>
    <br>`;
}

function updateLeagueTable(teamsData) {
    const leagueTableElement = document.getElementById("table-body");
    leagueTableElement.innerHTML = "";

    teamsData.sort((teamA, teamB) => -(teamA.points - teamB.points) + (0.01 * (teamA.goalDifference - teamB.goalDifference)) );

    teamIndex = 1;
    teamsData.forEach((element) =>{
        leagueTableElement.innerHTML += constructLeagueTableRowHTML(teamIndex, element);
        teamIndex++;
    });
}

function selectWeek() {
    const weekSelectionElement = document.getElementById("weekSelection");
    const resultsTableElement = document.getElementById("resultsTable-body");

    let selectedWeek = weekSelectionElement.value;
    if (selectedWeek == 0) {
        resultsTableElement.innerHTML = "";
    } else {
        let matches = fixture[selectedWeek - 1]
        let goals = matchRecordsForWeeks[selectedWeek - 1];

        resultsTableElement.innerHTML = constructMatchResultHTML(matches[0][0].name, goals[0][0], matches[0][1].name, goals[0][1]);
        resultsTableElement.innerHTML += constructMatchResultHTML(matches[1][0].name, goals[1][0], matches[1][1].name, goals[1][1]);
    }

    updateLeagueTable(teamsDataForWeeks[selectedWeek - 1])
}

function advance() {
    if (currentWeek >= 39) {
        return null;
    }

    const weekSelectionElement = document.getElementById("weekSelection");
    
    const resultsTableElement = document.getElementById("resultsTable-body");
    resultsTableElement.innerHTML = "";

    var teamsDataForCurrentWeek = [];
    var matchRecordsForCurrentWeek = [];
    var matchIndex = 0;
    fixture[currentWeek - 1].forEach(ABTeams => {
        AWinProbability = ABTeams[0].strength / ABTeams[1].strength
        BWinProbability = 1 / AWinProbability;
        let maxAGoals;
        let maxBGoals;
        if (AWinProbability >= BWinProbability) {
            maxAGoals = Math.min(5, Math.ceil((AWinProbability / (BWinProbability)) ** (0.4))) + 2;
            maxBGoals = Math.min(5, Math.ceil(((BWinProbability / (AWinProbability))) ** (0.7))) + 2;
        } else {
            maxAGoals = Math.min(5, Math.ceil((AWinProbability / (BWinProbability))) ** (0.7)) + 2;
            maxBGoals = Math.min(5, Math.ceil((BWinProbability / (AWinProbability)) ** (0.4))) + 2;
        }

        AGoals = Math.floor(Math.random() * maxAGoals);
        BGoals = Math.floor(Math.random() * maxBGoals);

        matchRecordsForCurrentWeek.push([AGoals, BGoals]);

        ABTeams[0].played++;
        ABTeams[1].played++;
        if (AGoals > BGoals){ ABTeams[0].won++; }
        else if(BGoals > AGoals){ ABTeams[1].won++; }
        else{ ABTeams[0].drawn++; ABTeams[1].drawn++; }
        ABTeams[0].goalsFor += AGoals;
        ABTeams[1].goalsFor += BGoals;
        ABTeams[0].goalsAgainst += BGoals;
        ABTeams[1].goalsAgainst += AGoals;

        teamsDataForCurrentWeek.push(ABTeams[0]);
        teamsDataForCurrentWeek.push(ABTeams[1]);

        resultsTableElement.innerHTML += constructMatchResultHTML(ABTeams[0].name, AGoals, ABTeams[1].name, BGoals)
        matchIndex++;
    });

    teamsDataForWeeks.push(teamsDataForCurrentWeek);
    matchRecordsForWeeks.push(matchRecordsForCurrentWeek);

    updateLeagueTable(teamsDataForCurrentWeek);

    weekSelectionElement.innerHTML +=
    `

    <option value="${currentWeek}">${currentWeek}. week</option>
    `

    document.getElementById("weekSelection").value = currentWeek++;
}

function advanceFinish() {
    for (let i = currentWeek; i <= 38; i++) {
        advance();
    }
}