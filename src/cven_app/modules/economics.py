from nicegui import ui

def content():
    ui.label('Engineering Economics').classes('text-h3 q-my-md')
    ui.markdown('''
    Engineering economics involves the systematic evaluation of the economic merits of proposed solutions to engineering problems.
    
    ### Key Concept: Time Value of Money
    Money has a time value because it can be invested and earn interest. Concepts like **Present Worth (P)**, **Future Worth (F)**, and **Uniform Series (A)** are fundamental.
    ''').classes('text-lg')

    with ui.card().classes('w-full p-6 shadow-lg'):
        ui.label('Equivalent Calculator').classes('text-h5 q-mb-md')
        
        with ui.row().classes('w-full gap-8'):
            with ui.column().classes('flex-1'):
                p_slider = ui.slider(min=0, max=10000, value=1000).props('label-always')
                ui.label('Present Value (P): $').bind_text_from(p_slider, 'value', backward=lambda v: f'{v:,.0f}')
                
                rate_slider = ui.slider(min=0, max=20, value=5, step=0.1).props('label-always')
                ui.label('Interest Rate (i): %').bind_text_from(rate_slider, 'value', backward=lambda v: f'{v:.1f}')
                
                years_slider = ui.slider(min=1, max=30, value=10).props('label-always')
                ui.label('Years (n): ').bind_text_from(years_slider, 'value')

            with ui.column().classes('flex-1 items-center justify-center bg-blue-50 rounded-lg p-4'):
                def calculate_future():
                    p = p_slider.value
                    i = rate_slider.value / 100
                    n = years_slider.value
                    return p * ((1 + i) ** n)

                result_label = ui.label('').classes('text-h4 text-blue-800 font-bold')
                ui.label('Estimated Future Value (F)').classes('text-subtitle1 text-blue-600')

                def update_result():
                    f = calculate_future()
                    result_label.text = f'${f:,.2f}'
                    chart.options['series'][0]['data'] = [p_slider.value * ((1 + rate_slider.value/100)**year) for year in range(int(years_slider.value) + 1)]
                    chart.update()

                p_slider.on('update:model-value', update_result)
                rate_slider.on('update:model-value', update_result)
                years_slider.on('update:model-value', update_result)

        # Echarts for visualization
        ui.label('Growth Projection').classes('text-h6 q-mt-lg')
        chart = ui.echart({
            'xAxis': {'type': 'category', 'data': [str(y) for y in range(31)], 'name': 'Year'},
            'yAxis': {'type': 'value', 'name': 'Value ($)'},
            'tooltip': {'trigger': 'axis'},
            'series': [{
                'data': [],
                'type': 'line',
                'smooth': True,
                'areaStyle': {'color': 'rgba(59, 130, 246, 0.2)'},
                'lineStyle': {'color': '#3b82f6', 'width': 4},
                'itemStyle': {'color': '#3b82f6'}
            }],
            'grid': {'left': '3%', 'right': '4%', 'bottom': '3%', 'containLabel': True}
        }).classes('w-full h-64')

        # Initial calculation
        update_result()
