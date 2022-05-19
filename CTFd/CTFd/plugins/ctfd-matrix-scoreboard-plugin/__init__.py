import os

from flask import (
    render_template,
    jsonify,
    Blueprint,
    url_for,
    session,
    redirect,
    request
)
from sqlalchemy.sql import or_

from CTFd import utils, scoreboard
from CTFd.models import db, Solves, Challenges
from CTFd.plugins import override_template
from CTFd.utils.config import is_scoreboard_frozen, ctf_theme, is_users_mode
from CTFd.utils.config.visibility import challenges_visible, scores_visible
from CTFd.utils.dates import (
    ctf_started, ctftime, view_after_ctf, unix_time_to_utc
)
from CTFd.utils.user import is_admin, authed

from pdb import set_trace as bp


def load(app):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(dir_path, 'scoreboard-matrix.html')
    override_template('scoreboard.html', open(template_path).read())

    matrix = Blueprint('matrix', __name__, static_folder='static')
    app.register_blueprint(matrix, url_prefix='/matrix')

    def get_standings():
        standings, (score_wise, award_wise, challenges) = scoreboard.get_standings(returnChallengeWiseScore=True)
        # Extract Categories from challenges
        categories = dict()
        challenge_to_cat = dict()
        for challenge in challenges:
            # bp()
            if challenge.category not in categories:
                categories[challenge.category] = []
            categories[challenge.category].append(challenge.id)
            challenge_to_cat[challenge.id] = challenge.category
         
        jchals = get_challenges()
        category_wise_chals = dict()
        for jchal in jchals:
            if jchal['category'] not in category_wise_chals:
                category_wise_chals[jchal['category']] = []
            category_wise_chals[jchal['category']].append(jchal['name'])
        
        team_cat_scores = dict()
        team_cat_solves = dict()

        for lis in [score_wise, award_wise]:
            for score in lis:
                team = score[0]
                if team not in team_cat_scores:
                    team_cat_scores[team] = dict()
                    for category in categories:
                        team_cat_scores[team][category] = 0
                if team not in team_cat_solves:
                    team_cat_solves[team] = dict()
                    for category in categories:
                        team_cat_solves[team][category] = 0
                chall = score[1]
                cat = challenge_to_cat[chall]
                if lis == score_wise:
                    team_cat_solves[team][cat] += 1
                team_cat_scores[team][cat] += score[2]
        
        for team in team_cat_solves:
            for cat in team_cat_solves[team]:
                if team_cat_solves[team][cat] == 0:
                    team_cat_solves[team][cat] = ''
                else:
                    team_cat_solves[team][cat] = '({}/{})'.format(team_cat_solves[team][cat], len(category_wise_chals[cat]))

        # bp()
        # TODO faster lookup here
        # bp() 
        jstandings = []



        for team in standings:
            teamid = team[0]
            # TODO: Handle dynamically chosing between user id and team id
            solves = db.session.query(Solves.challenge_id.label('challenge_id')).filter(Solves.user_id == teamid)
            freeze = utils.get_config('freeze')
            if freeze:
                freeze = unix_time_to_utc(freeze)
                if teamid != session.get('id'):
                    solves = solves.filter(Solves.date < freeze)
            solves = solves.all()
            jsolves = []
            for solve in solves:
                jsolves.append(solve.challenge_id)
            jstandings.append({'teamid': team[0], 'score': team[3], 'name': team[2], 'solves': jsolves})
        db.session.close()
        print('jchals are', get_challenges())
        # bp()
        return jstandings, team_cat_scores, categories, team_cat_solves

    def get_challenges():
        if not is_admin():
            if not ctftime():
                if view_after_ctf():
                    pass
                else:
                    return []
        if challenges_visible() and (ctf_started() or is_admin()):
            chals = db.session.query(
                Challenges.id,
                Challenges.name,
                Challenges.category
            ).filter(or_(Challenges.state != 'hidden', Challenges.state is None)).all()
            jchals = []
            for x in chals:
                jchals.append({
                    'id': x.id,
                    'name': x.name,
                    'category': x.category
                })

            # Sort into groups
            categories = set(map(lambda x: x['category'], jchals))
            jchals = [j for c in categories for j in jchals if j['category'] == c]
            return jchals
        return []

    def scoreboard_view():
        if scores_visible() and not authed():
            return redirect(url_for('auth.login', next=request.path))
        if not scores_visible():   
            return render_template('scoreboard.html',
                                   errors=['Scores are currently hidden'])
        standings, team_cat_scores, categories, team_cat_solves = get_standings()
        return render_template('scoreboard.html', standings=standings,
                               score_frozen=is_scoreboard_frozen(),
                               mode='users' if is_users_mode() else 'teams',
                               team_cat_scores = team_cat_scores, categories = categories, team_cat_solves = team_cat_solves,
                               challenges=get_challenges(), theme=ctf_theme())
  
    def scores():
        json = {'standings': []}
        if scores_visible() and not authed():
            return redirect(url_for('auth.login', next=request.path))
        if not scores_visible():
            return jsonify(json)

        standings = get_standings()

        for i, x in enumerate(standings):
            json['standings'].append({'pos': i + 1, 'id': x['name'], 'team': x['name'],
                                      'score': int(x['score']), 'solves': x['solves']})
        return jsonify(json)
     
    app.view_functions['scoreboard.listing'] = scoreboard_view
    app.view_functions['scoreboard.score'] = scores
