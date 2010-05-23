(function(){
	var oScript = document.getElementsByTagName("script")[document.getElementsByTagName("script").length-1];
	function closeIfr(){
			for (var i = 0; i < gAvailableImages.length; i++)
				removeEventListener(gAvailableImages[i].listener);
			removeEventListener(closeHandler);
			removeNode(byId("rensea__popup"));
			removeNode(oDiv);
			top.name = "";
			if(iTimer)clearInterval(iTimer);
			document.body.removeChild(oScript);
			oScript =undefined;
			return false;
	}
	function div(opt_parent) {
		var e = document.createElement("div");
		e.style.padding = "0";
		e.style.margin = "0";
		e.style.border = "0";
		e.style.position = "relative";
		if (opt_parent) {
		opt_parent.appendChild(e);
		}
		return e;
	}
	function cancelEvent(e) {
		e = e || window.event;
		if (e.preventDefault) {
			e.preventDefault();
		} else {
			e.returnValue = false;
		}
	}
	function addEventListener(instance, eventName, listener) {
		var listenerFn = listener;
		if (instance.addEventListener) {
			instance.addEventListener(eventName, listenerFn, false);
		} else if (instance.attachEvent) {
			listenerFn = function() {
				listener.call(instance, window.event);
			}
			instance.attachEvent("on" + eventName, listenerFn);
		} else {
			throw new Error("Event registration not supported");
		}
		return {
			instance: instance,
			name: eventName,
			listener: listenerFn
		};
	}
	function removeEventListener(o) {
		if(!o) return false;
		var instance = o.instance;
		if(instance)
			if(instance.removeEventListener) {
				instance.removeEventListener(o.name, o.listener, false);
			} else if (instance.detachEvent) {
				instance.detachEvent("on" + o.name, o.listener);
			}
	}
	function sendFrameMessage(m) {
		var p = "", iframe;
		for (var i in m) {
			if (!m.hasOwnProperty(i))
			continue;
			p += (p.length ? '&' : '');
			p += encodeURIComponent(i) + '=' + encodeURIComponent(m[i]);
		}
		if(p)	changeSrc(ifrSrc + '#' + p);
	}
	function onImageClick(image, e) {
		cancelEvent(e);
		// work around flickr photos with notes
		if(image.src == "http://l.yimg.com/g/images/spaceball.gif")
		image = image.previousSibling;
		sendFrameMessage({image:image.src, w:image.width, h:image.height});
	}
	function onImageMouseOver(image, e) {
		e = window.event || e;
		var popupContainer = byId("rensea__popup");
		popupContainer.style.display = "none";
		clearNode(popupContainer);
		var clickTarget = div(popupContainer);
		clickTarget.style.position = "absolute";
		var offset = getOffset(image);
		clickTarget.style.left = (offset.left - kOutlineSize + 1) + "px";
		clickTarget.style.top = (offset.top - kOutlineSize + 1) + "px";
		clickTarget.style.width = image.width + "px";
		clickTarget.style.height = image.height + "px";
		clickTarget.style.border = kOutlineSize + "px solid " + kOutlineColor;
		clickTarget.style.zoom = 1;
		clickTarget.style.cursor = "pointer";
		clickTarget.innerHTML = '<div style="margin:0;padding:0;width:100%;height:100%;position:relative;z-index:1;background-color:white;filter:alpha(opacity=1);opacity: 0.01"></div><div style="margin:0;position:absolute;top:0;left:0;background-color:white;padding:3px;color:#1030cc;border: 1px solid #1030cc;border-width: 0px 1px 1px 0px;z-index:2">' + '\u9009\u62E9\u5728\u4EBA\u95F4\u7F51\u4E0A\u7684\u914D\u56FE' + '</div>';
		addEventListener(clickTarget, "click", curry(onImageClick, image));
		addEventListener(clickTarget, "mouseout", onHoverMouseOut);
		popupContainer.style.display = "";
		cancelEvent(e);
	}
	function onHoverMouseOut(e) {
		e = window.event || e;
		oTarget = e.target || e.srcElement;
		if(oTarget.nodeType == 3) oTarget = oTarget.parentNode;
		var popupContainer = byId("rensea__popup");
		if (!popupContainer) return;
		var n = e.relatedTarget || (e.fromElement == oTarget ? e.toElement : e.fromElement);
	    while ( n && n != popupContainer )
			try { n = n.parentNode; }
			catch(e) { n = popupContainer; }
		if (n == popupContainer) return; // moused over child
		clearNode(popupContainer);
		popupContainer.style.display = "none";
		cancelEvent(e);
	}
	function byId(id) {
		return document.getElementById(id);
	}
	function scrollPos() {
		if (self.pageYOffset !== undefined) {
			return {
				x: self.pageXOffset,
				y: self.pageYOffset
			};
		}
		var d = document.documentElement||document.body;
		return {
			x: d.scrollLeft,
			y: d.scrollTop
		};
	}
	function setScrollPos(pos) {
		var e = document.documentElement, b = document.body;
		e.scrollLeft = b.scrollLeft = pos.x;
		e.scrollTop = b.scrollTop = pos.y;
	}
	function getOffset(obj) {
		var curleft = 0;
		var curtop = 0;
		if (obj.offsetParent) {
			curleft = obj.offsetLeft;
			curtop = obj.offsetTop;
			while (obj = obj.offsetParent) {
				curleft += obj.offsetLeft;
				curtop += obj.offsetTop;
			}
		}
		return {
			left: curleft,
			top: curtop
		};
	}
	function clearNode(node) {
		while (node.firstChild) {
			node.removeChild(node.firstChild);
		}
	}
	function removeNode(node) {
		if (node && node.parentNode) {
			node.parentNode.removeChild(node);
		}
	}
	function curry(method) {
		var curried = [];
			for (var i = 1; i < arguments.length; i++) {
			curried.push(arguments[i]);
		}
		return function() {
			var args = [];
			for (var i = 0; i < curried.length; i++) {
				args.push(curried[i]);
			}
			for (var i = 0; i < arguments.length; i++) {
				args.push(arguments[i]);
			}
			return method.apply(null, args);
		}
	}
	function changeSrc(sUrl){
		var oIframe = byId("rensea_iframe");
		try{
			oIframe.contentWindow.location.replace(sUrl);
		}catch(e){
			oIframe.contentWindow.location = sUrl;
		}
	}
	if(/http:\/\/(?:www\.)?renjian.com/i.test(window.location.href) || byId("rensea_iframe")) return false;
	var oHead = document.getElementsByTagName("head")[0];
	var oTitle = oHead.getElementsByTagName("title")[0];
	var oMeta = oHead.getElementsByTagName("meta");
	var title = oTitle.innerHTML, description = "";
	/*
	for(var i = 0, l = oMeta.length;  i < l; i++){
	   if(oMeta[i].getAttribute("name") && oMeta[i].getAttribute("name").toLowerCase() == "description"){
	      description = oMeta[i].getAttribute("content");
		  break;
	   }
	}*/
	if(!description){
		var oDes = document.getElementsByTagName("*");
		for(var j = 0, l = oDes.length; j < l; j++){
			if(oDes[j].nodeType == 1 && oDes[j].tagName == "H1"){
				description = oDes[j].innerHTML.replace(/<.*?\/?>/g, "");
				break;
			}
			if(oDes[j].nodeType == 1 && oDes[j].className.indexOf("description") != -1){
				description = oDes[j].innerHTML.replace(/<.*?\/?>/g, "");
				break;
			}
		}
		if(!description) description = title||"%20";
	}
	var oDiv = document.createElement("div"), ifrH = 278, isIe6 = /msie\s*6/i.test(navigator.userAgent);
	var ifrSrc = "http://renjian.com/dd/bookmarklet?title="+encodeURIComponent(title)+"&url="+encodeURIComponent(window.location.href)+"&des="+encodeURIComponent(description);
	oDiv.innerHTML = "<iframe style='position:absolute;width:100%; height:100%; left: 0; top: 0; z-index: -1; filter:alpha(opacity=0);opacity:0' ></iframe><div style='position: absolute; right: 8px; top: 8px; text-align: right;'><a id='closeBtn' style='font-size: 12px; text-decoration: underline; color: #0B7ECE;' href='javascript:void(0)'>\u5173\u95ED </a></div><iframe id='rensea_iframe' name='rensea_iframe' frameborder='0' scrolling='no'  width='100%' height='" + ifrH + "'></iframe>";
	with(oDiv.style){
		position = "absolute";
		top = (scrollPos().y||1)+"px";
		border = "3px solid #EBEAEA";
		width = "500px";
		right = "1px";
		background = "#fff";
		zIndex=100001;
	}
	document.body.insertBefore(oDiv, document.body.firstChild);
    changeSrc(ifrSrc);
	var oldScroll = scrollPos();
	location.replace(location.href.split("#")[0] + "#");
	setScrollPos(oldScroll);
	var closeHandler = addEventListener(byId("closeBtn"), "click",  closeIfr);
	var iTimer = setInterval(function(){
		//oDiv.style.top = (scrollPos().y||1) + "px";
		var hash = location.href.split('#')[1];
		if(hash){
			var h = hash.match(/height-\s*(\d+)/);
			var gCurScroll = scrollPos(); // save pos
			if(h && h[1]){
				byId("rensea_iframe").style.height = (ifrH+(h[1]|0||0)) + "px";
				gCurScroll = scrollPos(); // save pos
				location.replace(location.href.split("#")[0] + "#");
				setScrollPos(gCurScroll);
			}else if(hash.indexOf("minusH") > -1){
				byId("rensea_iframe").style.height = "128px";
				gCurScroll = scrollPos(); // save pos
				location.replace(location.href.split("#")[0] + "#");
				setScrollPos(gCurScroll);
			}else if(hash.indexOf("close") > -1 || top.name.indexOf("close") > -1){
		  		location.replace(location.href.split("#")[0] + "#");
		  		setScrollPos(gCurScroll);
		  		closeIfr();
		  	}
		}
	}, 16);
	window.onscroll = function(){
		oDiv.style.top = scrollPos().y + "px";
	};
	var popupContainer = div();
	popupContainer.id = "rensea__popup";
	popupContainer.style.position = "absolute";
	popupContainer.style.display = "none";
	popupContainer.style.left = "0px";
	popupContainer.style.top = "0px";
	popupContainer.style.zIndex = 99999;
	popupContainer.style.fontSize = "8pt";
	popupContainer.style.fontFamily = "Arial";
	popupContainer.style.fontStyle = "normal";
	popupContainer.style.fontWeight = "normal";
	popupContainer.style.background = "transparent";
	document.body.appendChild(popupContainer);
	// Highlight all the images on the page
	var kMinImageSize = 30;
	var kOutlineColor = "#1030cc";
	var kOutlineSize = 3;
	var gAvailableImages = [];
	var numImages = 0;
	var imageElements = document.getElementsByTagName("img");
	for (var i = 0; i < imageElements.length; i++) {
		var image = imageElements[i];
		if (image.width < kMinImageSize || image.height < kMinImageSize) {
			continue;
		}
		numImages++;
		var listener = addEventListener(image, "mouseover", curry(onImageMouseOver, image));
		gAvailableImages.push({
			element: image,
			cursor: image.style.cursor,
			listener: listener
		});
	}
})();