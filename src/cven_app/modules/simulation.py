from nicegui import ui
import numpy as np

def content():
    ui.label('Systems & Simulation').classes('text-h3 q-my-md')
    ui.markdown('''
    Simulation imitates real-world processes to account for **uncertainty**. Instead of using a single value (deterministic), we use **probability distributions** (stochastic).
    ''').classes('text-lg')

    with ui.tabs().classes('w-full') as tabs:
        t1 = ui.tab('Monte Carlo Simulation')
        t2 = ui.tab('Pareto Frontier')

    with ui.tab_panels(tabs, value=t1).classes('w-full bg-transparent'):
        with ui.tab_panel(t1):
            monte_carlo_tool()
        with ui.tab_panel(t2):
            pareto_frontier_tool()

def monte_carlo_tool():
    with ui.card().classes('w-full p-6 shadow-lg'):
        ui.label('Monte Carlo Simulation: Understanding Risk').classes('text-h5 q-mb-md')
        
        with ui.row().classes('w-full gap-8'):
            with ui.column().classes('w-80'):
                ui.label('1. Define Input Distribution').classes('font-bold')
                dist_type = ui.select(['Normal', 'Uniform', 'Poisson'], value='Normal', label='Distribution Type').classes('w-full')
                
                # Dynamic parameters based on distribution type
                params_container = ui.column().classes('w-full')
                
                @ui.refreshable
                def show_params():
                    if dist_type.value == 'Normal':
                        mean = ui.slider(min=0, max=1000, value=500).props('label-always')
                        ui.label(f'Mean (μ):').bind_text_from(mean, 'value', backward=lambda v: f'Mean (μ): {v}')
                        std = ui.slider(min=1, max=200, value=50).props('label-always')
                        ui.label(f'Std Dev (σ):').bind_text_from(std, 'value', backward=lambda v: f'Std Dev (σ): {v}')
                        return {'type': 'normal', 'loc': mean, 'scale': std}
                    elif dist_type.value == 'Uniform':
                        low = ui.slider(min=0, max=500, value=400).props('label-always')
                        ui.label(f'Min:').bind_text_from(low, 'value', backward=lambda v: f'Min: {v}')
                        high = ui.slider(min=501, max=1000, value=600).props('label-always')
                        ui.label(f'Max:').bind_text_from(high, 'value', backward=lambda v: f'Max: {v}')
                        return {'type': 'uniform', 'low': low, 'high': high}
                    else:
                        lam = ui.slider(min=1, max=50, value=10).props('label-always')
                        ui.label(f'Lambda (λ):').bind_text_from(lam, 'value', backward=lambda v: f'Lambda (λ): {v}')
                        return {'type': 'poisson', 'lam': lam}

                params_info = show_params()
                dist_type.on('update:model-value', show_params.refresh)

                ui.separator().classes('q-my-md')
                iterations = ui.number('Iterations', value=2000, min=100, max=10000, step=100).classes('w-full')
                run_btn = ui.button('Run Simulation', icon='play_arrow', on_click=lambda: run_sim()).classes('w-full q-mt-md')

            with ui.column().classes('flex-1'):
                stats_row = ui.row().classes('w-full justify-between q-mb-md p-4 bg-gray-50 rounded border')
                with stats_row:
                    with ui.column().classes('items-center'):
                        ui.label('Mean Output').classes('text-xs uppercase text-gray-500')
                        mean_label = ui.label('-').classes('text-xl font-bold')
                    with ui.column().classes('items-center'):
                        ui.label('95th Percentile').classes('text-xs uppercase text-gray-500')
                        p95_label = ui.label('-').classes('text-xl font-bold')
                    with ui.column().classes('items-center'):
                        ui.label('Std Deviation').classes('text-xs uppercase text-gray-500')
                        std_label = ui.label('-').classes('text-xl font-bold text-blue-600')

                chart = ui.echart({
                    'title': {'text': 'Outcome Distribution', 'left': 'center'},
                    'tooltip': {'trigger': 'axis', 'formatter': '{b} to {b1}: {c} count'},
                    'grid': {'left': '3%', 'right': '4%', 'bottom': '10%', 'containLabel': True},
                    'xAxis': {'type': 'category', 'name': 'Outcome Value', 'nameLocation': 'middle', 'nameGap': 25},
                    'yAxis': {'type': 'value', 'name': 'Frequency'},
                    'series': [{
                        'type': 'bar',
                        'barWidth': '95%',
                        'data': [],
                        'itemStyle': {'color': '#3b82f6', 'borderRadius': [4, 4, 0, 0]}
                    }]
                }).classes('w-full h-80')

        def run_sim():
            n = int(iterations.value)
            p = show_params() # Get current slider references from refreshable
            
            # Extract values from sliders/numbers correctly
            # Note: show_params returns the dict with component REFs
            # we need to ensure we get .value
            current_type = dist_type.value
            if current_type == 'Normal':
                data = np.random.normal(p['loc'].value, p['scale'].value, n)
            elif current_type == 'Uniform':
                data = np.random.uniform(p['low'].value, p['high'].value, n)
            else:
                data = np.random.poisson(p['lam'].value, n)

            # Statistics
            mean_label.text = f'{np.mean(data):.2f}'
            p95_label.text = f'{np.percentile(data, 95):.2f}'
            std_label.text = f'{np.std(data):.2f}'

            # Histogram bins
            counts, bins = np.histogram(data, bins=30)
            chart.options['xAxis']['data'] = [f'{bins[i]:.1f}' for i in range(len(bins)-1)]
            chart.options['series'][0]['data'] = counts.tolist()
            chart.update()

        # Initial run
        run_sim()

def pareto_frontier_tool():
    with ui.card().classes('w-full p-6 shadow-lg'):
        ui.label('Pareto Frontier: Conflicting Objectives').classes('text-h5 q-mb-md')
        ui.markdown('''
        In engineering, we often want to **Minimize Cost** while **Maximizing Reliability**. 
        The **Pareto Frontier** consists of all designs where you cannot improve one objective without making the other worse.
        ''')

        with ui.row().classes('w-full gap-8'):
            with ui.column().classes('w-80'):
                ui.label('1. Design Space Parameters').classes('font-bold')
                num_designs = ui.slider(min=50, max=500, value=200).props('label-always')
                ui.label('Number of Designs:').bind_text_from(num_designs, 'value')
                
                ui.separator().classes('q-my-md')
                ui.label('2. Trade-off Strength').classes('font-bold')
                correlation = ui.slider(min=-100, max=100, value=-50).props('label-always')
                ui.label('Correlation (Cost vs Reliability):').bind_text_from(correlation, 'value', backward=lambda v: f'{v}%')
                
                ui.button('Generate New Designs', icon='refresh', on_click=lambda: generate()).classes('w-full q-mt-md')

            with ui.column().classes('flex-1'):
                chart = ui.echart({
                    'title': {'text': 'Cost vs. Reliability Trade-off', 'left': 'center'},
                    'tooltip': {'trigger': 'item', 'formatter': 'Cost: {@[0]} <br/> Reliability: {@[1]}'},
                    'xAxis': {'type': 'value', 'name': 'Cost ($)', 'nameLocation': 'middle', 'nameGap': 25},
                    'yAxis': {'type': 'value', 'name': 'Reliability (%)', 'min': 0, 'max': 100},
                    'series': [
                        {
                            'name': 'All Designs',
                            'type': 'scatter',
                            'data': [],
                            'itemStyle': {'color': '#94a3b8', 'opacity': 0.6}
                        },
                        {
                            'name': 'Pareto Frontier',
                            'type': 'line',
                            'data': [],
                            'smooth': True,
                            'lineStyle': {'color': '#ef4444', 'width': 3},
                            'itemStyle': {'color': '#ef4444', 'borderWidth': 2},
                            'symbol': 'circle',
                            'symbolSize': 8
                        }
                    ],
                    'legend': {'bottom': 0}
                }).classes('w-full h-80')

        def generate():
            n = int(num_designs.value)
            corr = correlation.value / 100
            
            # Generate correlated random data
            # Cost (X) and Reliability (Y)
            # We want them generally inversely correlated for a clear frontier
            mean = [500, 70]
            cov = [[10000, corr * 100 * 10], [corr * 100 * 10, 100]]
            data = np.random.multivariate_normal(mean, cov, n)
            
            # Clip values to realistic bounds
            costs = np.clip(data[:, 0], 100, 1000)
            reliability = np.clip(data[:, 1], 10, 99)
            
            points = list(zip(costs, reliability))
            
            # Find Pareto Frontier (Assuming Min X, Max Y)
            # A point (x1, y1) dominates (x2, y2) if x1 <= x2 and y1 >= y2 (and at least one strict)
            sorted_points = sorted(points, key=lambda p: p[0]) # Sort by increasing cost
            pareto_set = []
            max_y = -1
            for x, y in sorted_points:
                if y > max_y:
                    pareto_set.append([float(x), float(y)])
                    max_y = y
            
            chart.options['series'][0]['data'] = [[float(x), float(y)] for x, y in points]
            chart.options['series'][1]['data'] = pareto_set
            chart.update()

        generate()
