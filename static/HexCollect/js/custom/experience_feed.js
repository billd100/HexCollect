// Canvas element in experience feed
window.onload = function() {
	var perc_eff = document.getElementById("percent_effectiveness");
	if (perc_eff.getContext) {
		var c = perc_eff.getContext('2d');
		var x = perc_eff.width * 0.5;
		var y = perc_eff.height * 0.5;

		var effectiveness = document.getElementById('percent').innerHTML;
		var percent = parseInt(effectiveness, 10);

		
		var radius = 45;
		var inner_radius = 32.5; // radius - lineWidth/2

		// inner circle
		c.beginPath()
		c.arc(x, y, inner_radius, 0, 3.14159*2);
		c.strokeStyle = '#eee';
		c.stroke()

		// text percent effective
		c.lineWidth = 25;
		c.font = "14px sans-serif";
		c.fillText("Effective", 55, 95, 115);
		c.font = "16px sans-serif";
		c.fillText(effectiveness, 27, 75, 115);
		c.font = "12px sans-serif"
		c.fillText("%", 86, 73, 115)
		
		// stroke percent effective
		c.beginPath()
		c.arc(x, y, radius, -3.14159/2, (2 * 3.14159 * percent/100) - 3.14159/2);
		c.strokeStyle = '#ddd';
		
		c.stroke()
	}
}
