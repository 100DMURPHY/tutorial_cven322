from nicegui import ui

def content():
    ui.label('Optimization Modeling').classes('text-h3 q-my-md')
    ui.markdown('''
    Optimization is the core of systems engineering. We aim to find the best possible solution given a set of constraints.
    
    ### Linear Programming (LP): Graphical Method
    For problems with two decision variables ($x_1$ and $x_2$), we can visualize the "Feasible Region" and find the optimal point.
    ''').classes('text-lg')

    with ui.card().classes('w-full p-6 shadow-lg'):
        ui.label('Graphical LP Solver (2 Variables)').classes('text-h5 q-mb-md')
        
        with ui.row().classes('w-full gap-8'):
            with ui.column().classes('w-64'):
                ui.label('Objective: Maximize Z = c1*x1 + c2*x2').classes('font-bold')
                c1 = ui.slider(min=0, max=10, value=3).props('label-always')
                ui.label('c1: ').bind_text_from(c1, 'value')
                c2 = ui.slider(min=0, max=10, value=5).props('label-always')
                ui.label('c2: ').bind_text_from(c2, 'value')

                ui.separator().classes('q-my-md')
                ui.label('Constraint: x1 + x2 ≤ b').classes('font-bold')
                limit = ui.slider(min=1, max=100, value=50).props('label-always')
                ui.label('Limit (b): ').bind_text_from(limit, 'value')

            with ui.column().classes('flex-1'):
                chart = ui.echart({
                    'xAxis': {'min': 0, 'max': 100, 'name': 'x1'},
                    'yAxis': {'min': 0, 'max': 100, 'name': 'x2'},
                    'series': [
                        {
                            'name': 'Feasible Region Boundary',
                            'type': 'line',
                            'data': [[0, 50], [50, 0]],
                            'areaStyle': {'color': 'rgba(34, 197, 94, 0.2)'},
                            'lineStyle': {'color': '#22c55e'}
                        },
                        {
                            'name': 'Objective Function',
                            'type': 'line',
                            'data': [[0, 30], [50, 0]],
                            'lineStyle': {'type': 'dashed', 'color': '#ef4444'}
                        }
                    ],
                    'legend': {'data': ['Feasible Region Boundary', 'Objective Function']},
                    'tooltip': {'trigger': 'axis'}
                }).classes('w-full h-80')

                def update_plot():
                    b = limit.value
                    # Constraint x1 + x2 <= b
                    chart.options['series'][0]['data'] = [[0, b], [b, 0]]
                    
                    # Objective c1*x1 + c2*x2 = Z
                    # We'll plot a representative line for Z (e.g., passing through half the feasible region)
                    current_c1 = c1.value
                    current_c2 = c2.value
                    if current_c2 > 0:
                        # Find Z at midpoint (b/2, b/2) or similar to show slope
                        z_sample = current_c1 * (b/2) + current_c2 * (b/2)
                        y_at_0 = z_sample / current_c2
                        x_at_0 = z_sample / current_c1 if current_c1 > 0 else 100
                        chart.options['series'][1]['data'] = [[0, y_at_0], [x_at_0, 0]]
                    
                    chart.update()
                    calculate_optimum()

                def calculate_optimum():
                    # For x1 + x2 <= b, Max Z = c1*x1 + c2*x2
                    # The optimum is always at a corner: (0,b) or (b,0) or (0,0)
                    b = limit.value
                    z_0_b = c2.value * b
                    z_b_0 = c1.value * b
                    
                    if z_0_b > z_b_0:
                        best_point = f"(0, {b})"
                        best_z = z_0_b
                    else:
                        best_point = f"({b}, 0)"
                        best_z = z_b_0
                    
                    opt_label.text = f'Optimal Solution: {best_point} | Max Z = {best_z}'

                opt_label = ui.label('').classes('text-lg font-bold text-center w-full q-mt-md text-green-700')
                
                c1.on('update:model-value', update_plot)
                c2.on('update:model-value', update_plot)
                limit.on('update:model-value', update_plot)
                
                update_plot()
