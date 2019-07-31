window.randomScalingFactor = function() {
  return 100
};
var colorNames = [
  // red:
  'rgb(255, 99, 132)',
  // orange:
  'rgb(255, 159, 64)',
  // yellow:
  'rgb(255, 205, 86)',
  // green:
  'rgb(75, 192, 192)',
  // blue:
  'rgb(54, 162, 235)',
  // purple:
  'rgb(153, 102, 255)',
  // grey:
  'rgb(201, 203, 207)'
]
var surveyColors =  {}
{% for question in  object.question_set.all %}
  surveyColors['{{ question.id }}'] =  'red';
{% endfor %}
var config = {
  type: 'bar',
  data: {
    labels: [],
    datasets: []
  },
  options: {
    elements: {
      point:{
          radius: 0
      }
    },
    responsive: true,
    title: {
      display: true,
      text: 'Survey'
    },
    tooltips: {
      mode: 'x-axis',
      intersect: false,
    },
    hover: {
      mode: 'nearest',
      intersect: true
    },
    legend: {
      display: true,
      position: 'bottom'
    },
    scales: {
        xAxes: [{
            ticks: {
                autoSkip: true,
                maxTicksLimit: 3
            }
        }],
       yAxes: [{
          beginAtZero: false
       }]
    }
  }
};
window.onload = function() {
  var ctx = document.getElementById('myChart').getContext('2d');
  window.myLine = new Chart(ctx, config);
  console.log("onload")
  console.log("{{ object.slug }}");
  loadData('{{ object.slug }}', 'year');
};
function toggleDataset(element, survey){
  console.log(survey);
  if (element !== undefined && element.classList.contains('active')) {
    element.classList.remove("active");
    removeDataset(survey);
  } else {
    element.classList.add("active");
    loadData(survey);
  }
}
function addDataset(data, labels, survey, maxLabels) {
    var colorIndex = surveyColors[survey];
    var newColor = colorNames[0];
    console.log(newColor);
    var newDataset = {
      label: survey,
      backgroundColor: newColor,
      borderColor: newColor,
      borderWidth: 4,
      lineTension: 0,
      data: data,
      fill: false
    };
    config.data.datasets.push(newDataset);
    config.data.labels = labels
    config.options.scales.xAxes = [{
      ticks: {
        autoSkip: true,
        maxTicksLimit: maxLabels
      }
    }]
    window.myLine.update();
}
function updateData(element, interval){
  document.getElementsByClassName("time active")[0].classList.remove("active");
  element.classList.add("active");
  var datasets = [...config.data.datasets];
  config.data.datasets = [];
  window.myLine.update();
  for (var i = 0; i < datasets.length; i++) {
    console.log(datasets[i].label);
    loadData(datasets[i].label, interval)
  }
}
function loadData(survey, interval){
    console.log(survey)
  interval = interval || document.getElementsByClassName("time active")[0].id;
  var xhr = typeof XMLHttpRequest != 'undefined'
    ? new XMLHttpRequest()
    : new ActiveXObject('Microsoft.XMLHTTP');
  xhr.open('GET', '/surveys/' + survey + '/questions.json?interval=' + interval);
  xhr.onload = function() {
      if (xhr.status === 200) {
          surveyInfo = JSON.parse(xhr.responseText);
          console.log(surveyInfo);
          var obj;
          var data = []
          var labels = []
          for (var i = 0; i < surveyInfo.data.length; i++) {
            obj = surveyInfo.data[i]
            data.push(parseFloat(obj.ask_value));
          }
          addDataset(surveyInfo.data, surveyInfo.labels, survey, surveyInfo.maxLabels)
      }
      else {
          alert('Request failed.  Returned status of ' + xhr.status);
      }
  };
  xhr.send();
}
function removeDataset(survey) {
  console.log(config.data.datasets);
  for (var i = 0; i < config.data.datasets.length; i++) {
    var obj = config.data.datasets[i];
    if (obj.label === survey){
      config.data.datasets.splice(i, 1);
    }
  }
  window.myLine.update();
}