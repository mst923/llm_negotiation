"""Prompt constants for all game types."""

SYSTEM_PROMPT = """\
You are playing a one-round game. You will be given instructions of the game.
"""

PERSONALITY_SYSTEM_MESSAGE = """\
You are given the following attributes of a person:
- Region: {region}
- Age: {age}
- Gender: {gender}

Based on these attributes, generate a plausible name and occupation for this person.
Output JSON with two keys: "name" and "occupation".
"""

ULTIMATUM_PROMPT = """\
Game Instructions:
In this game, you are the proposer (described below).
As the proposer, your task is to divide a sum of 100 dollars between
yourself and another player
Subsequently, another player (a responder) will then either accept or reject your proposal.
If they accept, then the money will be divided according to your proposal. If they reject, you two will earn nothing.

Now let us begin the game!
Recall that you are the proposer.

Please provide your answer in a single-line JSON format with three keys: "reasoning" and "decision" and "offer"
{"reasoning": "...", "decision": "...", "offer": "..."}

The value of "reasoning" should briefly explain your reasoning before making the decision.
The value of "decision" should have the following format: 'I keep [] dollars to myself
and offer [] dollars to the other player.'
Replace [] with your choices.
The value of "offer" shold be your proposed amount to the other player and it must be number


Subsequently, a responder will then either accept or reject your proposal.
If they accept, then the money will be divided according to your proposal.
If they reject,  you two will earn nothing.

Please answer in the exact format."""

DICTATOR_PROMPT = """\
Game Instructions:
In this game, you are the proposer (described below).
As the proposer, your task is to divide a sum of 100 dollars between
yourself and another player
Subsequently, another player (a responder) will then either accept or reject your proposal.
If they accept, then the money will be divided according to your proposal. If they reject, you will get the money based on your proposal, but they cannot get it.
In other words, you get the money based on your proposal whether they accept or reject it.
Therefore, they have no right of rejection.

Now let us begin the game!
Recall that you are the proposer.

Please provide your answer in a single-line JSON format with three keys: "reasoning" and "decision" and "offer"
{"reasoning": "...", "decision": "...", "offer": "..."}

The value of "reasoning" should briefly explain your reasoning before making the decision.
The value of "decision" should have the following format: 'I keep [] dollars to myself
and offer [] dollars to the other player.'
Replace [] with your choices.
The value of "offer" shold be your proposed amount to the other player and it must be number


Subsequently, a responder will then either accept or reject your proposal.
If they accept, then the money will be divided according to your proposal.
If they reject, you will get the money based on your proposal, but they cannot get it.
Recall you get the money based on your proposal whether they accept or reject it.
They have no right of rejection.

Please answer in the exact format."""

DICTATOR_ANONYMOUS_PROMPT = """\
Game Instructions:
In this game, you are the proposer (described below).
As the proposer, your task is to divide a sum of 100 dollars between
yourself and another player
Subsequently, another player (a responder) will then either accept or reject your proposal.
If they accept, then the money will be divided according to your proposal. If they reject, you will get the money based on your proposal, but they cannot get it.
In other words, you get the money based on your proposal whether they accept or reject it.
Therefore, they have no right of rejection.

And, in this game, the experimenter does not know who you are.
Whatever action you take, no one will know about it.

Now let us begin the game!
Recall that you are the proposer.

Please provide your answer in a single-line JSON format with three keys: "reasoning" and "decision" and "offer"
{"reasoning": "...", "decision": "...", "offer": "..."}

The value of "reasoning" should briefly explain your reasoning before making the decision.
The value of "decision" should have the following format: 'I keep [] dollars to myself
and offer [] dollars to the other player.'
Replace [] with your choices.
The value of "offer" shold be your proposed amount to the other player and it must be number


Subsequently, a responder will then either accept or reject your proposal.
If they accept, then the money will be divided according to your proposal.
If they reject, you will get the money based on your proposal, but they cannot get it.
Recall you get the money based on your proposal whether they accept or reject it.
They have no right of rejection.

Recall, in this game, the experimenter does not know who you are.
Whatever action you take, no one will know about it.

Please answer in the exact format."""

UNFAIR_RECEIVER_PROMPT = """\
Game Instructions:
In this game, you are the responder (described below).
Another player (the proposer) has proposed to divide 100 dollars.
The proposer offers you 10 dollars and keeps 90 dollars for themselves.

You must decide whether to accept or reject this proposal.
If you accept, the money will be divided as proposed.
If you reject, neither of you will receive anything.

Please provide your answer in a single-line JSON format with two keys: "reasoning" and "decision"
{"reasoning": "...", "decision": "..."}

The value of "reasoning" should briefly explain your reasoning before making the decision.
The value of "decision" should be either "accept" or "reject".

Please answer in the exact format."""

UNFAIR_RECEIVER_COMPUTER_PROMPT = """\
Game Instructions:
In this game, you are the responder (described below).
A computer program has proposed to divide 100 dollars.
The computer program offers you 10 dollars and keeps 90 dollars for itself.

You must decide whether to accept or reject this proposal.
If you accept, the money will be divided as proposed.
If you reject, neither of you will receive anything.

Please provide your answer in a single-line JSON format with two keys: "reasoning" and "decision"
{"reasoning": "...", "decision": "..."}

The value of "reasoning" should briefly explain your reasoning before making the decision.
The value of "decision" should be either "accept" or "reject".

Please answer in the exact format."""
