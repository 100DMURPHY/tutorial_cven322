from nicegui import ui

def content():
    ui.label('Optimization Modeling').classes('text-h3 q-my-md')
    ui.markdown('''
    Optimization is the core of systems engineering. We aim to find the best possible solution given a set of constraints.
    
    ### Linear Programming (LP): Graphical Method
    For problems with two decision variables ($x_1$ and $x_2$), we can visualize the "Feasible Region" and find the optimal point.
    ''').classes('text-lg')

    with ui.tabs().classes('w-full') as tabs:
        t1 = ui.tab('Graphical LP Solver')
        t2 = ui.tab('Sensitivity Analysis')
        t3 = ui.tab('Network Modeling')
        t4 = ui.tab('Simplex Tableau')

    with ui.tab_panels(tabs, value=t1).classes('w-full bg-transparent'):
        with ui.tab_panel(t1):
            graphical_lp_tool()
        with ui.tab_panel(t2):
            sensitivity_analysis_tool()
        with ui.tab_panel(t3):
            network_module()
        with ui.tab_panel(t4):
            simplex_tableau_tool()

def graphical_lp_tool():
    with ui.card().classes('w-full p-6 shadow-lg'):
        ui.label('Graphical LP Solver (2 Variables, 2 Constraints)').classes('text-h5 q-mb-md')
        
        with ui.row().classes('w-full gap-8'):
            with ui.column().classes('w-80'):
                ui.label('Objective: Max Z = c1*x1 + c2*x2').classes('font-bold')
                c1 = ui.slider(min=0, max=10, value=3).props('label-always')
                ui.label('c1 (x1 coeff):').bind_text_from(c1, 'value')
                c2 = ui.slider(min=0, max=10, value=5).props('label-always')
                ui.label('c2 (x2 coeff):').bind_text_from(c2, 'value')

                ui.separator().classes('q-my-md')
                ui.label('Constraint 1: x1 + x2 ≤ b1').classes('font-bold text-blue-600')
                b1 = ui.slider(min=10, max=100, value=50).props('label-always')
                ui.label('Limit (b1):').bind_text_from(b1, 'value')

                ui.label('Constraint 2: 2x1 + x2 ≤ b2').classes('font-bold text-orange-600')
                b2 = ui.slider(min=10, max=150, value=80).props('label-always')
                ui.label('Limit (b2):').bind_text_from(b2, 'value')

            with ui.column().classes('flex-1'):
                chart = ui.echart({
                    'xAxis': {'min': 0, 'max': 100, 'name': 'x1'},
                    'yAxis': {'min': 0, 'max': 100, 'name': 'x2'},
                    'series': [
                        {
                            'name': 'Constraint 1',
                            'type': 'line',
                            'data': [],
                            'lineStyle': {'color': '#3b82f6', 'width': 2}
                        },
                        {
                            'name': 'Constraint 2',
                            'type': 'line',
                            'data': [],
                            'lineStyle': {'color': '#f59e0b', 'width': 2}
                        },
                        {
                            'name': 'Feasible Region',
                            'type': 'line',
                            'data': [],
                            'areaStyle': {'color': 'rgba(34, 197, 94, 0.2)'},
                            'lineStyle': {'width': 0}
                        },
                        {
                            'name': 'Optimal Point',
                            'type': 'scatter',
                            'data': [],
                            'itemStyle': {'color': '#ef4444', 'borderWidth': 2},
                            'symbolSize': 12
                        }
                    ],
                    'legend': {'data': ['Constraint 1', 'Constraint 2', 'Feasible Region', 'Optimal Point'], 'bottom': 0},
                    'tooltip': {'trigger': 'axis'}
                }).classes('w-full h-80')

                def update():
                    v_b1 = b1.value
                    v_b2 = b2.value
                    v_c1 = c1.value
                    v_c2 = c2.value
                    
                    # Constraint lines
                    # C1: x1 + x2 = b1 -> (0, b1), (b1, 0)
                    chart.options['series'][0]['data'] = [[0, v_b1], [v_b1, 0]]
                    # C2: 2x1 + x2 = b2 -> (0, b2), (b2/2, 0)
                    chart.options['series'][1]['data'] = [[0, v_b2], [v_b2/2, 0]]
                    
                    # Corner points for feasible region
                    # 1. (0, 0)
                    # 2. (0, min(b1, b2))
                    # 3. Intersection of C1 and C2:
                    #    x1 + x2 = b1
                    #    2x1 + x2 = b2
                    #    Subtracting: x1 = b2 - b1
                    #    Then: x2 = b1 - (b2 - b1) = 2b1 - b2
                    inter_x = v_b2 - v_b1
                    inter_y = 2*v_b1 - v_b2
                    
                    corners = [[0, 0]]
                    if v_b1 < v_b2: # C1 starts lower on Y
                         corners.append([0, v_b1])
                    else:
                         corners.append([0, v_b2])
                    
                    # Add intersection if it's in the first quadrant
                    if inter_x > 0 and inter_y > 0:
                        corners.append([inter_x, inter_y])
                        
                    if v_b1 < v_b2/2: # C1 ends lower on X
                        corners.append([v_b1, 0])
                    else:
                        corners.append([v_b2/2, 0])
                    
                    # Sort corners by angle to ensure polygon is drawn correctly
                    # (Simplified here since we know the order for 2 constraints)
                    feasible_data = sorted(corners, key=lambda p: (p[1]/p[0] if p[0]>0 else 999), reverse=True)
                    feasible_data.append([0,0]) # Close the loop
                    
                    chart.options['series'][2]['data'] = feasible_data
                    
                    # Solve
                    best_z = -1
                    best_p = [0, 0]
                    for px, py in corners:
                        z = v_c1 * px + v_c2 * py
                        if z > best_z:
                            best_z = z
                            best_p = [px, py]
                    
                    chart.options['series'][3]['data'] = [best_p]
                    chart.update()
                    opt_label.text = f'Optimal Solution: ({best_p[0]:.1f}, {best_p[1]:.1f}) | Max Z = {best_z:.1f}'

                opt_label = ui.label('').classes('text-lg font-bold text-center w-full q-mt-md text-green-700')
                
                for s in [c1, c2, b1, b2]:
                    s.on('update:model-value', update)
                update()

def sensitivity_analysis_tool():
    with ui.card().classes('w-full p-6 shadow-lg'):
        ui.label('Sensitivity Analysis: Shadow Prices').classes('text-h5 q-mb-md')
        ui.markdown('''
        **Shadow Price** tells us how much the optimal objective value ($Z$) would increase if we increased a constraint limit by **one unit**.
        ''')
        
        with ui.row().classes('w-full gap-8'):
            with ui.column().classes('w-80'):
                ui.label('Vary Limit b1 (Constraint 1)').classes('font-bold')
                base_b1 = ui.slider(min=10, max=100, value=50).props('label-always')
                
                ui.separator().classes('q-my-md')
                ui.label('Fixed Parameters').classes('text-xs text-gray-500')
                ui.label('c1=3, c2=5, b2=80')

            with ui.column().classes('flex-1'):
                chart = ui.echart({
                    'title': {'text': 'Z vs. b1 Limit', 'left': 'center'},
                    'xAxis': {'type': 'value', 'name': 'b1 Limit'},
                    'yAxis': {'type': 'value', 'name': 'Optimal Z'},
                    'series': [{
                        'type': 'line',
                        'data': [],
                        'smooth': True,
                        'lineStyle': {'color': '#3b82f6', 'width': 3},
                        'markPoint': {'data': [{'type': 'max', 'name': 'Max'}]}
                    }],
                    'tooltip': {'trigger': 'axis'}
                }).classes('w-full h-64')
                
                shadow_price_box = ui.row().classes('w-full justify-center gap-4 q-mt-md')
                with shadow_price_box:
                    with ui.card().classes('bg-blue-50 p-2 items-center'):
                        ui.label('Shadow Price (b1)').classes('text-xs uppercase')
                        sp_label = ui.label('0.0').classes('text-h6 font-bold')

        def calculate_sensitivity():
            # Fixed values
            v_c1, v_c2 = 3, 5
            v_b2 = 80
            
            # Range for b1
            b1_range = list(range(10, 101, 2))
            z_values = []
            
            for v_b1 in b1_range:
                # Same corner logic as above
                inter_x = v_b2 - v_b1
                inter_y = 2*v_b1 - v_b2
                corners = [[0, 0], [0, min(v_b1, v_b2)], [v_b2/2 if v_b2/2 < v_b1 else v_b1, 0]]
                if inter_x > 0 and inter_y > 0:
                    corners.append([inter_x, inter_y])
                
                z = max(v_c1 * px + v_c2 * py for px, py in corners)
                z_values.append([v_b1, round(z, 2)])
            
            chart.options['series'][0]['data'] = z_values
            chart.update()
            
            # Local shadow price (numerical derivative near current slider value)
            curr_b = base_b1.value
            def get_z(b):
                ix = v_b2 - b
                iy = 2*b - v_b2
                crs = [[0, 0], [0, min(b, v_b2)], [v_b2/2 if v_b2/2 < b else b, 0]]
                if ix > 0 and iy > 0: crs.append([ix, iy])
                return max(v_c1 * px + v_c2 * py for px, py in crs)
            
            sp = (get_z(curr_b + 0.1) - get_z(curr_b)) / 0.1
            sp_label.text = f'{sp:.1f}'

        base_b1.on('update:model-value', calculate_sensitivity)
        calculate_sensitivity()

def network_module():
    with ui.card().classes('w-full p-6 shadow-lg'):
        ui.label('Network Modeling: CPM Analysis').classes('text-h5 q-mb-md')
        ui.markdown('''
        Critical Path Method (CPM) identifies the longest path of planned activities to the end of the project. 
        It calculates early/late starts and identifies "Slack" for each task.
        ''')

        # Define graph
        nodes = [
            {'name': 'A', 'x': 50, 'y': 250},
            {'name': 'B', 'x': 200, 'y': 100},
            {'name': 'C', 'x': 200, 'y': 400},
            {'name': 'D', 'x': 350, 'y': 100},
            {'name': 'E', 'x': 350, 'y': 400},
            {'name': 'F', 'x': 500, 'y': 250},
        ]
        
        links = [
            {'source': 'A', 'target': 'B', 'weight': 4},
            {'source': 'A', 'target': 'C', 'weight': 2},
            {'source': 'B', 'target': 'D', 'weight': 5},
            {'source': 'C', 'target': 'B', 'weight': 1},
            {'source': 'C', 'target': 'E', 'weight': 8},
            {'source': 'D', 'target': 'F', 'weight': 3},
            {'source': 'E', 'target': 'D', 'weight': 2},
            {'source': 'E', 'target': 'F', 'weight': 6},
        ]

        chart = ui.echart({
            'title': {'text': 'Node-Link Diagram', 'left': 'center'},
            'tooltip': {},
            'series': [{
                'type': 'graph',
                'layout': 'none',
                'symbolSize': 40,
                'roam': True,
                'label': {'show': True},
                'edgeSymbol': ['circle', 'arrow'],
                'edgeSymbolSize': [4, 10],
                'edgeLabel': {'show': True, 'formatter': '{@weight}'},
                'data': [{'name': n['name'], 'x': n['x'], 'y': n['y']} for n in nodes],
                'links': [{'source': l['source'], 'target': l['target'], 'weight': l['weight']} for l in links],
                'lineStyle': {'opacity': 0.9, 'width': 2, 'curveness': 0}
            }]
        }).classes('w-full h-96')

        def solve_cpm():
            # Forward Pass: ES (Earliest Start)
            es = {n['name']: 0 for n in nodes}
            for n_name in ['A', 'B', 'C', 'D', 'E', 'F']:
                incoming = [l for l in links if l['target'] == n_name]
                if incoming:
                    es[n_name] = max(es[l['source']] + l['weight'] for l in incoming)
            
            # Backward Pass: LS (Latest Start)
            duration = es['F']
            ls = {n['name']: duration for n in nodes}
            for n_name in reversed(['A', 'B', 'C', 'D', 'E', 'F']):
                outgoing = [l for l in links if l['source'] == n_name]
                if outgoing:
                    ls[n_name] = min(ls[l['target']] - l['weight'] for l in outgoing)
            
            slack = {name: ls[name] - es[name] for name in es}
            
            new_links = []
            for l in links:
                is_critical = (slack[l['source']] == 0 and slack[l['target']] == 0 and 
                              es[l['target']] - es[l['source']] == l['weight'])
                new_links.append({
                    'source': l['source'],
                    'target': l['target'],
                    'weight': l['weight'],
                    'lineStyle': {'color': '#ef4444' if is_critical else '#ccc', 'width': 4 if is_critical else 2}
                })
            
            chart.options['series'][0]['links'] = new_links
            chart.update()
            res_label.text = f'Project Duration: {duration} | Critical Path Highlighted in Red'
            ui.notify(f"Node Info (ES/LS/Slack): " + ", ".join([f"{k}: {es[k]}/{ls[k]}/{slack[k]}" for k in es]))

        ui.button('Run CPM Analysis', icon='alt_route', on_click=solve_cpm).classes('w-full q-mt-md')
        res_label = ui.label('').classes('text-center w-full font-bold text-red-600 q-mt-md')

def simplex_tableau_tool():
    with ui.card().classes('w-full p-6 shadow-lg'):
        ui.label('Simplex Tableau Visualizer').classes('text-h5 q-mb-md')
        ui.markdown('''
        The Simplex algorithm moves between corner points. This tool shows the tableau for: 
        **Max Z = 3x1 + 5x2** subject to **x1 + x2 ≤ 50** and **2x1 + x2 ≤ 80**.
        ''')
        
        with ui.row().classes('w-full justify-center'):
            step = ui.number('Simplex Step', value=0, min=0, max=2, precision=0).classes('w-32')
            ui.label('Change step to see pivoting iterations').classes('text-gray-500 self-center')
        
        @ui.refreshable
        def show_tableau():
            s = int(step.value)
            columns = [{'name': c, 'label': c, 'field': c} for c in ['Basis', 'x1', 'x2', 's1', 's2', 'RHS']]
            if s == 0:
                rows = [
                    {'Basis': 's1', 'x1': 1, 'x2': 1, 's1': 1, 's2': 0, 'RHS': 50},
                    {'Basis': 's2', 'x1': 2, 'x2': 1, 's1': 0, 's2': 1, 'RHS': 80},
                    {'Basis': 'Z', 'x1': -3, 'x2': -5, 's1': 0, 's2': 0, 'RHS': 0}
                ]
            elif s == 1:
                rows = [
                    {'Basis': 'x2', 'x1': 1, 'x2': 1, 's1': 1, 's2': 0, 'RHS': 50},
                    {'Basis': 's2', 'x1': 1, 'x2': 0, 's1': -1, 's2': 1, 'RHS': 30},
                    {'Basis': 'Z', 'x1': 2, 'x2': 0, 's1': 5, 's2': 0, 'RHS': 250}
                ]
            else:
                rows = [
                    {'Basis': 'x2', 'x1': 0, 'x2': 1, 's1': 2, 's2': -1, 'RHS': 20},
                    {'Basis': 'x1', 'x1': 1, 'x2': 0, 's1': -1, 's2': 1, 'RHS': 30},
                    {'Basis': 'Z', 'x1': 0, 'x2': 0, 's1': 7, 's2': -2, 'RHS': 190}
                ]
            ui.table(columns=columns, rows=rows).classes('w-full')

        show_tableau()
        step.on('update:model-value', show_tableau.refresh)
