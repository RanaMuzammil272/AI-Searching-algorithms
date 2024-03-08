!pip install igraph
from random import randint
import igraph
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go


class InvestmentOption:
    def __init__(self, name, expected_return, risk):
        self.name = name
        self.expected_return = expected_return
        self.risk = risk

class Node:
    def __init__(self, investment_option, remaining_budget, risk_tolerance, investment_horizon, value=None):
        self.investment_option = investment_option
        self.remaining_budget = remaining_budget
        self.risk_tolerance = risk_tolerance
        self.investment_horizon = investment_horizon
        self.value = value
        self.children = []

def evaluate_node(node):
    val=node.investment_option.expected_return*node.remaining_budget-node.investment_option.risk*node.remaining_budget
    node.value=val


def generate_possible_moves(root):
    if(is_terminal(root)):
        return
    no_of_childs=randint(1, 3)
    for i in range(no_of_childs):
      descision=randint(1, 3)
      if(descision==1):
        temp=randint(1, 5)
        profit=root.investment_option.expected_return+temp
        name=root.investment_option.name
        loss=root.investment_option.risk
        remaining_budget=root.remaining_budget
        tolerance=root.risk_tolerance
        level=root.investment_horizon-1
        obj1=InvestmentOption(name,profit,loss)
        child=Node(obj1,remaining_budget,tolerance,level)
        evaluate_node(child)
        root.children.append(child)
        generate_possible_moves(child)
      elif(descision==2):
        loss=randint(1, 5)
        profit=root.investment_option.expected_return
        name=root.investment_option.name
        new_risk=root.investment_option.risk+loss
        remaining_budget=root.investment_option.risk*root.remaining_budget
        remaining_budget-=root.remaining_budget
        tolerance=root.risk_tolerance
        level=root.investment_horizon-1
        obj1=InvestmentOption(name,profit,new_risk)
        child=Node(obj1,remaining_budget,tolerance,level)
        evaluate_node(child)
        root.children.append(child)
        generate_possible_moves(child)
      elif(descision==3):
        profit=root.investment_option.expected_return
        name=root.investment_option.name
        loss=root.investment_option.risk
        remaining_budget=root.remaining_budget
        tolerance=root.risk_tolerance
        level=root.investment_horizon-1
        obj1=InvestmentOption(name,profit,loss)
        child=Node(obj1,remaining_budget,tolerance,level)
        evaluate_node(child)
        root.children.append(child)
        generate_possible_moves(child)

def is_terminal(node):
    if(node.investment_horizon>0):
      return False
    return True

def against_rules(node):
    if(node.investment_option.risk > node.risk_tolerance):
      return True
    return False

def minimax(node, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_terminal(node) or against_rules(node):
        return node.value

    if maximizing_player:
        max_value = float('-inf')
        for child in node.children:
            value = minimax(child, depth - 1, alpha, beta, False)
            max_value = max(max_value, value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break  # Beta cutoff
        return max_value
    else:
        min_value = float('inf')
        for child in node.children:
            value = minimax(child, depth - 1, alpha, beta, True)
            min_value = min(min_value, value)
            beta = min(beta, value)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_value


def get_best_move(options, initial_budget, risk_tolerance, investment_horizon):
    best_value = float('-inf')
    best_option = None
    roots = []

    for option in options:
        root = Node(option, initial_budget, risk_tolerance, investment_horizon)
        generate_possible_moves(root)
        roots.append(root)

        value = minimax(root, depth=root.investment_horizon, alpha=float('-inf'), beta=float('inf'), maximizing_player=False)

        if value > best_value:
            best_value = value
            best_option = option

    return best_value, best_option, roots
def construct_graph(root):
    g = Graph(directed=True)
    queue = [(root, -1)]  # (node, parent_index)
    while queue:
        current_node, parent_index = queue.pop(0)
        g.add_vertex(name=str(current_node.value))
        if parent_index != -1:
            g.add_edge(parent_index, g.vcount() - 1)
        for child in current_node.children:
            queue.append((child, g.vcount() - 1))
    return g

def plot_tree(root):
    G = construct_graph(root)
    lay = G.layout('rt')

    position = {k: lay[k] for k in range(len(lay))}
    Y = [lay[k][1] for k in range(len(lay))]
    M = max(Y)

    es = EdgeSeq(G)  # sequence of edges
    E = [e.tuple for e in G.es]  # list of edges

    Xn = [position[k][0] for k in range(len(position))]
    Yn = [2 * M - position[k][1] for k in range(len(position))]
    Xe = []
    Ye = []
    for edge in E:
        Xe += [position[edge[0]][0], position[edge[1]][0], None]
        Ye += [2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1], None]

    labels = [str(v) for v in range(len(position))]
    hover_texts = []

    def traverse_tree(node):
        if not node:
            return
        hover_texts.append(f"Node: {node.value}<br>"
                           f"Investment Option: {node.investment_option.name}<br>"
                           f"Expected Return: {node.investment_option.expected_return}<br>"
                           f"Risk: {node.investment_option.risk}<br>"
                           f"Remaining Budget: {node.remaining_budget}<br>"
                           f"Risk Tolerance: {node.risk_tolerance}<br>"
                           f"Investment Horizon: {node.investment_horizon}")
        for child in node.children:
            traverse_tree(child)

    traverse_tree(root)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Xe,
                             y=Ye,
                             mode='lines',
                             line=dict(color='rgb(210,210,210)', width=1),
                             hoverinfo='none'
                             ))
    fig.add_trace(go.Scatter(x=Xn,
                             y=Yn,
                             mode='markers',
                             name='bla',
                             marker=dict(symbol='circle-dot',
                                         size=32,  # change node size here
                                         color='#6175c1',  # '#DB4551',
                                         line=dict(color='rgb(50,50,50)', width=1)
                                         ),
                             text=labels,
                             hoverinfo='text',
                             opacity=0.8
                             ))

    def make_annotations(pos, text, font_size=10, font_color='rgb(250,250,250)'):
        L = len(pos)
        if len(text) != L:
            raise ValueError('The lists pos and text must have the same len')
        annotations = []
        for k in range(L):
            annotations.append(
                dict(
                    text=labels[k],
                    x=pos[k][0], y=2 * M - position[k][1],
                    xref='x1', yref='y1',
                    font=dict(color=font_color, size=font_size),
                    showarrow=False)
            )
        return annotations

    axis = dict(showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                )

    fig.update_layout(title='Tree with Reingold-Tilford Layout',
                      annotations=make_annotations(position, labels),
                      font_size=12,
                      showlegend=False,
                      xaxis=axis,
                      yaxis=axis,
                      margin=dict(l=40, r=40, b=85, t=100),
                      hovermode='closest',
                      plot_bgcolor='rgb(248,248,248)'
                      )

    fig.update_traces(hovertext=hover_texts)

    fig.show()
options = [
    InvestmentOption(name='Stocks', expected_return=0.1, risk=0.05),
    InvestmentOption(name='Bonds', expected_return=0.05, risk=0.02),
    InvestmentOption(name='Real Estate', expected_return=0.08, risk=0.03)
]

# Initial parameters
initial_budget = 10000
risk_tolerance = 0.5
investment_horizon = 5

# Find the best move (portfolio allocation)
best_value, best_option, roots = get_best_move(options, initial_budget, risk_tolerance, investment_horizon)

# Print the recommended portfolio allocation
print("Recommended Portfolio Allocation:", best_option.name)
print("Max Profit Achievable:", best_value)
for root in roots:
  plot_tree(root)

