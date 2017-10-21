function formatValue(value) {
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}

function generateChart(path) {
  c3.generate({
    bindto: '#chart-' + path.slug,
    data: {
      json: path.graph_data,
      x: 'date',
      xFormat: '%Y-%m-%dT%H:%M:%S.%L',
      keys: {
        x: 'date',
        value: ['value']
      },
      names: {
        value: path.label
      }
    },
    color: {
      pattern: ['#212529']
    },
    legend: {
      show: false
    },
    axis: {
      y: {
        show: false
      },
      x: {
        show: false,
        type: 'timeseries',
        tick: {
          format: '%Y-%m-%d %I%p UTC'
        }
      }
    }
  });
}
