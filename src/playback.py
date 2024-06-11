# from flask import Blueprint, g, redirect, url_for, jsonify
# from spotifysetup import get_spotify

# playback_bp = Blueprint('playback', __name__)

# @playback_bp.before_request
# def before_request():
#     g.sp = get_spotify()

# #playback features
# @playback_bp.route('/Pause')
# def Pause():
#     if g.sp is None:
#         return redirect(url_for("login", _external=True))
#     g.sp.pause_playback()
#     return jsonify({"data": "successful pause"})

# @playback_bp.route('/Resume')
# def Resume():
#     if g.sp is None:
#         return redirect(url_for("login", _external=True))
#     g.sp.start_playback()
#     return jsonify({"data": "successful resume"})

# @playback_bp.route('/Previous')
# def Previous():
#     if g.sp is None:
#         return redirect(url_for("login", _external=True))
#     g.sp.previous_track()
#     return jsonify({"data": "successful prev"})

# @playback_bp.route('/Next')
# def Next():
#     if g.sp is None:
#         return redirect(url_for("login", _external=True))
#     g.sp.next_track()
#     return jsonify({"data": "successful next"})
