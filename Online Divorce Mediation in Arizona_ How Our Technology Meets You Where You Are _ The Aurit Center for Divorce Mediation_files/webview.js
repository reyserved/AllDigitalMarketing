(() => {
var Fi=Object.defineProperty,Wi=Object.defineProperties;var Ui=Object.getOwnPropertyDescriptors;var It=Object.getOwnPropertySymbols;var qi=Object.prototype.hasOwnProperty,ji=Object.prototype.propertyIsEnumerable;var zt=(b,v,y)=>v in b?Fi(b,v,{enumerable:!0,configurable:!0,writable:!0,value:y}):b[v]=y,S=(b,v)=>{for(var y in v||(v={}))qi.call(v,y)&&zt(b,y,v[y]);if(It)for(var y of It(v))ji.call(v,y)&&zt(b,y,v[y]);return b},W=(b,v)=>Wi(b,Ui(v));(function(){"use strict";var $;const b="modulepreload",v=function(i){return"/"+i},y={},me=function(e,t,n){let o=Promise.resolve();function s(r){const c=new Event("vite:preloadError",{cancelable:!0});if(c.payload=r,window.dispatchEvent(c),!c.defaultPrevented)throw r}return o.then(r=>{for(const c of r||[])c.status==="rejected"&&s(c.reason);return e().catch(s)})},De=(i,e)=>[...e.querySelectorAll(i)],Pt=i=>{const t=new DOMParser().parseFromString(i,"text/html");return{head:t.querySelector("head"),body:t.querySelector("body")}},Bt=(i,e,t)=>{const n=new RegExp(`heyflow\\[(?:'|")${e}(?:'|")\\]`,"g"),o=`heyflow['${t}']`;i.head.innerHTML=i.head.innerHTML.replace(n,o),i.body.innerHTML=i.body.innerHTML.replace(n,o);const s=i.head.querySelector("#window-props");return s&&(s.innerHTML=s.innerHTML.replace(e,t)),i},Fe=()=>{const i=document.querySelectorAll("heyflow-wrapper");return Array.from(i).reduce((e,t)=>{const n=t.getAttribute("flow-id");return n&&e.push(n),e},[])},Lt=()=>({VITE_FLOW_URL_PATTERN:"https://mini-serve.prd.heyflow.com/[FLOW_ID]",VITE_API_ENDPOINT:"https://api.prd.heyflow.com"}),Mt=i=>{for(const[e,t]of Object.entries(i))if(t===void 0)throw new Error(`Missing variable ${e} in env`);return i},Nt=Lt(),We=Mt(Nt),{VITE_API_ENDPOINT:Ht}=We,ne=({flowID:i,embeddedFlowIDs:e,message:t,severity:n,data:o,embedIndex:s,source:r})=>{const c=S({flowID:i,embeddedFlowIDs:e,message:t,severity:n,userAgent:window.navigator.userAgent,hostname:window.location.hostname,pathname:window.location.pathname,embedIndex:s,clientTimestamp:new Date().toISOString(),source:r,sessionID:void 0},o?{data:o}:{});setTimeout(async()=>{var l,h;if(s!==void 0){const d=window.heyflow[`${i}-${s}`];console.log({embedIndex:s,s:d.runtime.sessionId}),c.sessionID=d.runtime.sessionId}const a=`${Ht}/widget/logs`;if(typeof((l=window==null?void 0:window.navigator)==null?void 0:l.sendBeacon)=="function"){window.navigator.sendBeacon(a,JSON.stringify(c))?console.debug("[Widget Logs] Successfully sent log via sendBeacon"):console.warn("[Widget Logs] Failed to send log via sendBeacon");return}console.debug("[Widget Logs] Sending log via fetch"),await fetch(a,{method:"POST",headers:{"Content-Type":"application/json","x-heyflow-session-id":(h=c.sessionID)!=null?h:""},body:JSON.stringify(c)}).catch(d=>{console.error("Error sending widget log:",d,a,c)})},100)},C=({message:i,error:e,flowID:t,embedIndex:n,source:o})=>{const s={message:i,severity:"error",data:{error:`${e.name} ${e.message}`}};if(t)ne(W(S({},s),{flowID:t,embedIndex:n,source:o}));else{const r=Fe();r.length>0&&ne(W(S({},s),{embeddedFlowIDs:r,source:o}))}};window.addEventListener("unhandledrejection",i=>{var n;const e=(n=i.reason)==null?void 0:n.stack;if(!(e!=null&&e.includes("/webview.js")))return;const t=Fe();t.length>0&&ne({embeddedFlowIDs:t,message:"Unhandled rejection",severity:"error",data:{error:`${i.reason}`},source:"unknown"})}),me(()=>Promise.resolve().then(()=>ei),void 0).then(i=>i.default()).catch(i=>{console.error(i),C({message:"Failed to import loader-element",error:i,source:"loader"})}),me(()=>Promise.resolve().then(()=>ai),void 0).then(i=>i.default()).catch(i=>{console.error(i),C({message:"Failed to import modal-element",error:i,source:"modal"})}),me(()=>Promise.resolve().then(()=>Ni),void 0).then(i=>i.default()).catch(i=>{console.error(i),C({message:"Failed to import heyflow-wrapper",error:i,source:"embed"})});const oe=window,we=oe.ShadowRoot&&(oe.ShadyCSS===void 0||oe.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,ge=Symbol(),Ue=new WeakMap;let qe=class{constructor(e,t,n){if(this._$cssResult$=!0,n!==ge)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e,this.t=t}get styleSheet(){let e=this.o;const t=this.t;if(we&&e===void 0){const n=t!==void 0&&t.length===1;n&&(e=Ue.get(t)),e===void 0&&((this.o=e=new CSSStyleSheet).replaceSync(this.cssText),n&&Ue.set(t,e))}return e}toString(){return this.cssText}};const je=i=>new qe(typeof i=="string"?i:i+"",void 0,ge),ye=(i,...e)=>{const t=i.length===1?i[0]:e.reduce(((n,o,s)=>n+(r=>{if(r._$cssResult$===!0)return r.cssText;if(typeof r=="number")return r;throw Error("Value passed to 'css' function must be a 'css' function result: "+r+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(o)+i[s+1]),i[0]);return new qe(t,i,ge)},Dt=(i,e)=>{we?i.adoptedStyleSheets=e.map((t=>t instanceof CSSStyleSheet?t:t.styleSheet)):e.forEach((t=>{const n=document.createElement("style"),o=oe.litNonce;o!==void 0&&n.setAttribute("nonce",o),n.textContent=t.cssText,i.appendChild(n)}))},Ve=we?i=>i:i=>i instanceof CSSStyleSheet?(e=>{let t="";for(const n of e.cssRules)t+=n.cssText;return je(t)})(i):i;var be;const se=window,Ge=se.trustedTypes,Ft=Ge?Ge.emptyScript:"",Je=se.reactiveElementPolyfillSupport,_e={toAttribute(i,e){switch(e){case Boolean:i=i?Ft:null;break;case Object:case Array:i=i==null?i:JSON.stringify(i)}return i},fromAttribute(i,e){let t=i;switch(e){case Boolean:t=i!==null;break;case Number:t=i===null?null:Number(i);break;case Object:case Array:try{t=JSON.parse(i)}catch(n){t=null}}return t}},Ke=(i,e)=>e!==i&&(e==e||i==i),$e={attribute:!0,type:String,converter:_e,reflect:!1,hasChanged:Ke},Ee="finalized";let U=class extends HTMLElement{constructor(){super(),this._$Ei=new Map,this.isUpdatePending=!1,this.hasUpdated=!1,this._$El=null,this._$Eu()}static addInitializer(e){var t;this.finalize(),((t=this.h)!==null&&t!==void 0?t:this.h=[]).push(e)}static get observedAttributes(){this.finalize();const e=[];return this.elementProperties.forEach(((t,n)=>{const o=this._$Ep(n,t);o!==void 0&&(this._$Ev.set(o,n),e.push(o))})),e}static createProperty(e,t=$e){if(t.state&&(t.attribute=!1),this.finalize(),this.elementProperties.set(e,t),!t.noAccessor&&!this.prototype.hasOwnProperty(e)){const n=typeof e=="symbol"?Symbol():"__"+e,o=this.getPropertyDescriptor(e,n,t);o!==void 0&&Object.defineProperty(this.prototype,e,o)}}static getPropertyDescriptor(e,t,n){return{get(){return this[t]},set(o){const s=this[e];this[t]=o,this.requestUpdate(e,s,n)},configurable:!0,enumerable:!0}}static getPropertyOptions(e){return this.elementProperties.get(e)||$e}static finalize(){if(this.hasOwnProperty(Ee))return!1;this[Ee]=!0;const e=Object.getPrototypeOf(this);if(e.finalize(),e.h!==void 0&&(this.h=[...e.h]),this.elementProperties=new Map(e.elementProperties),this._$Ev=new Map,this.hasOwnProperty("properties")){const t=this.properties,n=[...Object.getOwnPropertyNames(t),...Object.getOwnPropertySymbols(t)];for(const o of n)this.createProperty(o,t[o])}return this.elementStyles=this.finalizeStyles(this.styles),!0}static finalizeStyles(e){const t=[];if(Array.isArray(e)){const n=new Set(e.flat(1/0).reverse());for(const o of n)t.unshift(Ve(o))}else e!==void 0&&t.push(Ve(e));return t}static _$Ep(e,t){const n=t.attribute;return n===!1?void 0:typeof n=="string"?n:typeof e=="string"?e.toLowerCase():void 0}_$Eu(){var e;this._$E_=new Promise((t=>this.enableUpdating=t)),this._$AL=new Map,this._$Eg(),this.requestUpdate(),(e=this.constructor.h)===null||e===void 0||e.forEach((t=>t(this)))}addController(e){var t,n;((t=this._$ES)!==null&&t!==void 0?t:this._$ES=[]).push(e),this.renderRoot!==void 0&&this.isConnected&&((n=e.hostConnected)===null||n===void 0||n.call(e))}removeController(e){var t;(t=this._$ES)===null||t===void 0||t.splice(this._$ES.indexOf(e)>>>0,1)}_$Eg(){this.constructor.elementProperties.forEach(((e,t)=>{this.hasOwnProperty(t)&&(this._$Ei.set(t,this[t]),delete this[t])}))}createRenderRoot(){var e;const t=(e=this.shadowRoot)!==null&&e!==void 0?e:this.attachShadow(this.constructor.shadowRootOptions);return Dt(t,this.constructor.elementStyles),t}connectedCallback(){var e;this.renderRoot===void 0&&(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),(e=this._$ES)===null||e===void 0||e.forEach((t=>{var n;return(n=t.hostConnected)===null||n===void 0?void 0:n.call(t)}))}enableUpdating(e){}disconnectedCallback(){var e;(e=this._$ES)===null||e===void 0||e.forEach((t=>{var n;return(n=t.hostDisconnected)===null||n===void 0?void 0:n.call(t)}))}attributeChangedCallback(e,t,n){this._$AK(e,n)}_$EO(e,t,n=$e){var o;const s=this.constructor._$Ep(e,n);if(s!==void 0&&n.reflect===!0){const r=(((o=n.converter)===null||o===void 0?void 0:o.toAttribute)!==void 0?n.converter:_e).toAttribute(t,n.type);this._$El=e,r==null?this.removeAttribute(s):this.setAttribute(s,r),this._$El=null}}_$AK(e,t){var n;const o=this.constructor,s=o._$Ev.get(e);if(s!==void 0&&this._$El!==s){const r=o.getPropertyOptions(s),c=typeof r.converter=="function"?{fromAttribute:r.converter}:((n=r.converter)===null||n===void 0?void 0:n.fromAttribute)!==void 0?r.converter:_e;this._$El=s,this[s]=c.fromAttribute(t,r.type),this._$El=null}}requestUpdate(e,t,n){let o=!0;e!==void 0&&(((n=n||this.constructor.getPropertyOptions(e)).hasChanged||Ke)(this[e],t)?(this._$AL.has(e)||this._$AL.set(e,t),n.reflect===!0&&this._$El!==e&&(this._$EC===void 0&&(this._$EC=new Map),this._$EC.set(e,n))):o=!1),!this.isUpdatePending&&o&&(this._$E_=this._$Ej())}async _$Ej(){this.isUpdatePending=!0;try{await this._$E_}catch(t){Promise.reject(t)}const e=this.scheduleUpdate();return e!=null&&await e,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){var e;if(!this.isUpdatePending)return;this.hasUpdated,this._$Ei&&(this._$Ei.forEach(((o,s)=>this[s]=o)),this._$Ei=void 0);let t=!1;const n=this._$AL;try{t=this.shouldUpdate(n),t?(this.willUpdate(n),(e=this._$ES)===null||e===void 0||e.forEach((o=>{var s;return(s=o.hostUpdate)===null||s===void 0?void 0:s.call(o)})),this.update(n)):this._$Ek()}catch(o){throw t=!1,this._$Ek(),o}t&&this._$AE(n)}willUpdate(e){}_$AE(e){var t;(t=this._$ES)===null||t===void 0||t.forEach((n=>{var o;return(o=n.hostUpdated)===null||o===void 0?void 0:o.call(n)})),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(e)),this.updated(e)}_$Ek(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$E_}shouldUpdate(e){return!0}update(e){this._$EC!==void 0&&(this._$EC.forEach(((t,n)=>this._$EO(n,this[n],t))),this._$EC=void 0),this._$Ek()}updated(e){}firstUpdated(e){}};U[Ee]=!0,U.elementProperties=new Map,U.elementStyles=[],U.shadowRootOptions={mode:"open"},Je==null||Je({ReactiveElement:U}),((be=se.reactiveElementVersions)!==null&&be!==void 0?be:se.reactiveElementVersions=[]).push("1.6.3");var Se;const re=window,q=re.trustedTypes,Xe=q?q.createPolicy("lit-html",{createHTML:i=>i}):void 0,Ae="$lit$",T=`lit$${(Math.random()+"").slice(9)}$`,Ye="?"+T,Wt=`<${Ye}>`,P=document,K=()=>P.createComment(""),X=i=>i===null||typeof i!="object"&&typeof i!="function",Ze=Array.isArray,Ut=i=>Ze(i)||typeof(i==null?void 0:i[Symbol.iterator])=="function",xe=`[ 	
\f\r]`,Y=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,Qe=/-->/g,et=/>/g,B=RegExp(`>|${xe}(?:([^\\s"'>=/]+)(${xe}*=${xe}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`,"g"),tt=/'/g,it=/"/g,nt=/^(?:script|style|textarea|title)$/i,qt=i=>(e,...t)=>({_$litType$:i,strings:e,values:t}),k=qt(1),R=Symbol.for("lit-noChange"),f=Symbol.for("lit-nothing"),ot=new WeakMap,L=P.createTreeWalker(P,129,null,!1);function st(i,e){if(!Array.isArray(i)||!i.hasOwnProperty("raw"))throw Error("invalid template strings array");return Xe!==void 0?Xe.createHTML(e):e}const jt=(i,e)=>{const t=i.length-1,n=[];let o,s=e===2?"<svg>":"",r=Y;for(let c=0;c<t;c++){const a=i[c];let l,h,d=-1,u=0;for(;u<a.length&&(r.lastIndex=u,h=r.exec(a),h!==null);)u=r.lastIndex,r===Y?h[1]==="!--"?r=Qe:h[1]!==void 0?r=et:h[2]!==void 0?(nt.test(h[2])&&(o=RegExp("</"+h[2],"g")),r=B):h[3]!==void 0&&(r=B):r===B?h[0]===">"?(r=o!=null?o:Y,d=-1):h[1]===void 0?d=-2:(d=r.lastIndex-h[2].length,l=h[1],r=h[3]===void 0?B:h[3]==='"'?it:tt):r===it||r===tt?r=B:r===Qe||r===et?r=Y:(r=B,o=void 0);const p=r===B&&i[c+1].startsWith("/>")?" ":"";s+=r===Y?a+Wt:d>=0?(n.push(l),a.slice(0,d)+Ae+a.slice(d)+T+p):a+T+(d===-2?(n.push(void 0),c):p)}return[st(i,s+(i[t]||"<?>")+(e===2?"</svg>":"")),n]};class Z{constructor({strings:e,_$litType$:t},n){let o;this.parts=[];let s=0,r=0;const c=e.length-1,a=this.parts,[l,h]=jt(e,t);if(this.el=Z.createElement(l,n),L.currentNode=this.el.content,t===2){const d=this.el.content,u=d.firstChild;u.remove(),d.append(...u.childNodes)}for(;(o=L.nextNode())!==null&&a.length<c;){if(o.nodeType===1){if(o.hasAttributes()){const d=[];for(const u of o.getAttributeNames())if(u.endsWith(Ae)||u.startsWith(T)){const p=h[r++];if(d.push(u),p!==void 0){const E=o.getAttribute(p.toLowerCase()+Ae).split(T),w=/([.?@])?(.*)/.exec(p);a.push({type:1,index:s,name:w[2],strings:E,ctor:w[1]==="."?Gt:w[1]==="?"?Kt:w[1]==="@"?Xt:ae})}else a.push({type:6,index:s})}for(const u of d)o.removeAttribute(u)}if(nt.test(o.tagName)){const d=o.textContent.split(T),u=d.length-1;if(u>0){o.textContent=q?q.emptyScript:"";for(let p=0;p<u;p++)o.append(d[p],K()),L.nextNode(),a.push({type:2,index:++s});o.append(d[u],K())}}}else if(o.nodeType===8)if(o.data===Ye)a.push({type:2,index:s});else{let d=-1;for(;(d=o.data.indexOf(T,d+1))!==-1;)a.push({type:7,index:s}),d+=T.length-1}s++}}static createElement(e,t){const n=P.createElement("template");return n.innerHTML=e,n}}function j(i,e,t=i,n){var o,s,r,c;if(e===R)return e;let a=n!==void 0?(o=t._$Co)===null||o===void 0?void 0:o[n]:t._$Cl;const l=X(e)?void 0:e._$litDirective$;return(a==null?void 0:a.constructor)!==l&&((s=a==null?void 0:a._$AO)===null||s===void 0||s.call(a,!1),l===void 0?a=void 0:(a=new l(i),a._$AT(i,t,n)),n!==void 0?((r=(c=t)._$Co)!==null&&r!==void 0?r:c._$Co=[])[n]=a:t._$Cl=a),a!==void 0&&(e=j(i,a._$AS(i,e.values),a,n)),e}class Vt{constructor(e,t){this._$AV=[],this._$AN=void 0,this._$AD=e,this._$AM=t}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(e){var t;const{el:{content:n},parts:o}=this._$AD,s=((t=e==null?void 0:e.creationScope)!==null&&t!==void 0?t:P).importNode(n,!0);L.currentNode=s;let r=L.nextNode(),c=0,a=0,l=o[0];for(;l!==void 0;){if(c===l.index){let h;l.type===2?h=new Q(r,r.nextSibling,this,e):l.type===1?h=new l.ctor(r,l.name,l.strings,this,e):l.type===6&&(h=new Yt(r,this,e)),this._$AV.push(h),l=o[++a]}c!==(l==null?void 0:l.index)&&(r=L.nextNode(),c++)}return L.currentNode=P,s}v(e){let t=0;for(const n of this._$AV)n!==void 0&&(n.strings!==void 0?(n._$AI(e,n,t),t+=n.strings.length-2):n._$AI(e[t])),t++}}class Q{constructor(e,t,n,o){var s;this.type=2,this._$AH=f,this._$AN=void 0,this._$AA=e,this._$AB=t,this._$AM=n,this.options=o,this._$Cp=(s=o==null?void 0:o.isConnected)===null||s===void 0||s}get _$AU(){var e,t;return(t=(e=this._$AM)===null||e===void 0?void 0:e._$AU)!==null&&t!==void 0?t:this._$Cp}get parentNode(){let e=this._$AA.parentNode;const t=this._$AM;return t!==void 0&&(e==null?void 0:e.nodeType)===11&&(e=t.parentNode),e}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(e,t=this){e=j(this,e,t),X(e)?e===f||e==null||e===""?(this._$AH!==f&&this._$AR(),this._$AH=f):e!==this._$AH&&e!==R&&this._(e):e._$litType$!==void 0?this.g(e):e.nodeType!==void 0?this.$(e):Ut(e)?this.T(e):this._(e)}k(e){return this._$AA.parentNode.insertBefore(e,this._$AB)}$(e){this._$AH!==e&&(this._$AR(),this._$AH=this.k(e))}_(e){this._$AH!==f&&X(this._$AH)?this._$AA.nextSibling.data=e:this.$(P.createTextNode(e)),this._$AH=e}g(e){var t;const{values:n,_$litType$:o}=e,s=typeof o=="number"?this._$AC(e):(o.el===void 0&&(o.el=Z.createElement(st(o.h,o.h[0]),this.options)),o);if(((t=this._$AH)===null||t===void 0?void 0:t._$AD)===s)this._$AH.v(n);else{const r=new Vt(s,this),c=r.u(this.options);r.v(n),this.$(c),this._$AH=r}}_$AC(e){let t=ot.get(e.strings);return t===void 0&&ot.set(e.strings,t=new Z(e)),t}T(e){Ze(this._$AH)||(this._$AH=[],this._$AR());const t=this._$AH;let n,o=0;for(const s of e)o===t.length?t.push(n=new Q(this.k(K()),this.k(K()),this,this.options)):n=t[o],n._$AI(s),o++;o<t.length&&(this._$AR(n&&n._$AB.nextSibling,o),t.length=o)}_$AR(e=this._$AA.nextSibling,t){var n;for((n=this._$AP)===null||n===void 0||n.call(this,!1,!0,t);e&&e!==this._$AB;){const o=e.nextSibling;e.remove(),e=o}}setConnected(e){var t;this._$AM===void 0&&(this._$Cp=e,(t=this._$AP)===null||t===void 0||t.call(this,e))}}class ae{constructor(e,t,n,o,s){this.type=1,this._$AH=f,this._$AN=void 0,this.element=e,this.name=t,this._$AM=o,this.options=s,n.length>2||n[0]!==""||n[1]!==""?(this._$AH=Array(n.length-1).fill(new String),this.strings=n):this._$AH=f}get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}_$AI(e,t=this,n,o){const s=this.strings;let r=!1;if(s===void 0)e=j(this,e,t,0),r=!X(e)||e!==this._$AH&&e!==R,r&&(this._$AH=e);else{const c=e;let a,l;for(e=s[0],a=0;a<s.length-1;a++)l=j(this,c[n+a],t,a),l===R&&(l=this._$AH[a]),r||(r=!X(l)||l!==this._$AH[a]),l===f?e=f:e!==f&&(e+=(l!=null?l:"")+s[a+1]),this._$AH[a]=l}r&&!o&&this.j(e)}j(e){e===f?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,e!=null?e:"")}}class Gt extends ae{constructor(){super(...arguments),this.type=3}j(e){this.element[this.name]=e===f?void 0:e}}const Jt=q?q.emptyScript:"";class Kt extends ae{constructor(){super(...arguments),this.type=4}j(e){e&&e!==f?this.element.setAttribute(this.name,Jt):this.element.removeAttribute(this.name)}}class Xt extends ae{constructor(e,t,n,o,s){super(e,t,n,o,s),this.type=5}_$AI(e,t=this){var n;if((e=(n=j(this,e,t,0))!==null&&n!==void 0?n:f)===R)return;const o=this._$AH,s=e===f&&o!==f||e.capture!==o.capture||e.once!==o.once||e.passive!==o.passive,r=e!==f&&(o===f||s);s&&this.element.removeEventListener(this.name,this,o),r&&this.element.addEventListener(this.name,this,e),this._$AH=e}handleEvent(e){var t,n;typeof this._$AH=="function"?this._$AH.call((n=(t=this.options)===null||t===void 0?void 0:t.host)!==null&&n!==void 0?n:this.element,e):this._$AH.handleEvent(e)}}class Yt{constructor(e,t,n){this.element=e,this.type=6,this._$AN=void 0,this._$AM=t,this.options=n}get _$AU(){return this._$AM._$AU}_$AI(e){j(this,e)}}const rt=re.litHtmlPolyfillSupport;rt==null||rt(Z,Q),((Se=re.litHtmlVersions)!==null&&Se!==void 0?Se:re.litHtmlVersions=[]).push("2.8.0");const Zt=(i,e,t)=>{var n,o;const s=(n=t==null?void 0:t.renderBefore)!==null&&n!==void 0?n:e;let r=s._$litPart$;if(r===void 0){const c=(o=t==null?void 0:t.renderBefore)!==null&&o!==void 0?o:null;s._$litPart$=r=new Q(e.insertBefore(K(),c),c,void 0,t!=null?t:{})}return r._$AI(i),r};var Oe,Ce;class M extends U{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){var e,t;const n=super.createRenderRoot();return(e=(t=this.renderOptions).renderBefore)!==null&&e!==void 0||(t.renderBefore=n.firstChild),n}update(e){const t=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(e),this._$Do=Zt(t,this.renderRoot,this.renderOptions)}connectedCallback(){var e;super.connectedCallback(),(e=this._$Do)===null||e===void 0||e.setConnected(!0)}disconnectedCallback(){var e;super.disconnectedCallback(),(e=this._$Do)===null||e===void 0||e.setConnected(!1)}render(){return R}}M.finalized=!0,M._$litElement$=!0,(Oe=globalThis.litElementHydrateSupport)===null||Oe===void 0||Oe.call(globalThis,{LitElement:M});const at=globalThis.litElementPolyfillSupport;at==null||at({LitElement:M}),((Ce=globalThis.litElementVersions)!==null&&Ce!==void 0?Ce:globalThis.litElementVersions=[]).push("3.3.3");function Te(i,e){customElements.get(i)===void 0&&customElements.define(i,e)}const Qt=()=>Te("loader-element",le),Le=class Le extends M{render(){return k`<div>
      <svg
        id="dots"
        width="75px"
        height="16px"
        viewBox="0 0 132 70"
        version="1.1"
        xmlns="http://www.w3.org/2000/svg"
      >
        <title>dots</title>
        <defs></defs>
        <g
          id="Page-1"
          stroke="none"
          stroke-width="1"
          fill="darkgrey"
          fill-rule="evenodd"
        >
          <g id="dots">
            <circle id="dot1" cx="-40" cy="35" r="35"></circle>
            <circle id="dot2" cx="65" cy="35" r="35"></circle>
            <circle id="dot3" cx="165" cy="35" r="35"></circle>
          </g>
        </g>
      </svg>
    </div>`}};Le.styles=ye`
    div {
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      gap: 2rem;
    }
    img {
      width: 8rem;
    }
    #dots #dot1 {
      animation: load 0.8s infinite;
    }
    #dots #dot2 {
      animation: load 0.8s infinite;
      animation-delay: 0.1s;
    }
    #dots #dot3 {
      animation: load 0.8s infinite;
      animation-delay: 0.2s;
    }
    @keyframes load {
      0% {
        opacity: 0;
      }
      50% {
        opacity: 1;
      }
      100% {
        opacity: 0;
      }
    }
  `;let le=Le;const ei=Object.freeze(Object.defineProperty({__proto__:null,LoaderElement:le,default:Qt},Symbol.toStringTag,{value:"Module"}));const ti=(i,e)=>e.kind==="method"&&e.descriptor&&!("value"in e.descriptor)?W(S({},e),{finisher(t){t.createProperty(e.key,i)}}):{kind:"field",key:Symbol(),placement:"own",descriptor:{},originalKey:e.key,initializer(){typeof e.initializer=="function"&&(this[e.key]=e.initializer.call(this))},finisher(t){t.createProperty(e.key,i)}},ii=(i,e,t)=>{e.constructor.createProperty(t,i)};function m(i){return(e,t)=>t!==void 0?ii(i,e,t):ti(i,e)}function de(i){return m(W(S({},i),{state:!0}))}var ke;((ke=window.HTMLSlotElement)===null||ke===void 0?void 0:ke.prototype.assignedElements)!=null;const lt={ATTRIBUTE:1},dt=i=>(...e)=>({_$litDirective$:i,values:e});let ct=class{constructor(e){}get _$AU(){return this._$AM._$AU}_$AT(e,t,n){this._$Ct=e,this._$AM=t,this._$Ci=n}_$AS(e,t){return this.update(e,t)}update(e,t){return this.render(...t)}};const ee=dt(class extends ct{constructor(i){var e;if(super(i),i.type!==lt.ATTRIBUTE||i.name!=="class"||((e=i.strings)===null||e===void 0?void 0:e.length)>2)throw Error("`classMap()` can only be used in the `class` attribute and must be the only part in the attribute.")}render(i){return" "+Object.keys(i).filter((e=>i[e])).join(" ")+" "}update(i,[e]){var t,n;if(this.it===void 0){this.it=new Set,i.strings!==void 0&&(this.nt=new Set(i.strings.join(" ").split(/\s/).filter((s=>s!==""))));for(const s in e)e[s]&&!(!((t=this.nt)===null||t===void 0)&&t.has(s))&&this.it.add(s);return this.render(e)}const o=i.element.classList;this.it.forEach((s=>{s in e||(o.remove(s),this.it.delete(s))}));for(const s in e){const r=!!e[s];r===this.it.has(s)||!((n=this.nt)===null||n===void 0)&&n.has(s)||(r?(o.add(s),this.it.add(s)):(o.remove(s),this.it.delete(s)))}return R}});const ht="important",ni=" !"+ht,ut=dt(class extends ct{constructor(i){var e;if(super(i),i.type!==lt.ATTRIBUTE||i.name!=="style"||((e=i.strings)===null||e===void 0?void 0:e.length)>2)throw Error("The `styleMap` directive must be used in the `style` attribute and must be the only part in the attribute.")}render(i){return Object.keys(i).reduce(((e,t)=>{const n=i[t];return n==null?e:e+`${t=t.includes("-")?t:t.replace(/(?:^(webkit|moz|ms|o)|)(?=[A-Z])/g,"-$&").toLowerCase()}:${n};`}),"")}update(i,[e]){const{style:t}=i.element;if(this.ht===void 0){this.ht=new Set;for(const n in e)this.ht.add(n);return this.render(e)}this.ht.forEach((n=>{e[n]==null&&(this.ht.delete(n),n.includes("-")?t.removeProperty(n):t[n]="")}));for(const n in e){const o=e[n];if(o!=null){this.ht.add(n);const s=typeof o=="string"&&o.endsWith(ni);n.includes("-")||s?t.setProperty(n,s?o.slice(0,-11):o,s?ht:""):t[n]=o}}return R}}),oi=`@keyframes slideInFromBottom {
  0% {
    opacity: 0;
    transform: translateY(20%);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideOutToBottom {
  0% {
    opacity: 1;
    transform: translateY(0);
  }
  100% {
    opacity: 0;
    transform: translateY(20%);
  }
}

.hey__modal-wrapper {
  margin: 0 auto;
  position: absolute;
  left: -10000px;
  top: 0;
  width: 100%;
  height: 100%;
  z-index: -10000;
}

.hey__modal-wrapper-visible {
  visibility: visible !important;
  z-index: 1000;
  left: 0;
}

.hey__modal {
  position: fixed;
  opacity: 0;
  top: 0;
  left: 0;
  z-index: 1001;
  transition: top 0.2s;
}

.hey__modal_web-component {
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  max-width: 100vw;
}

.hey__modal-web-component-wrapper {
  position: absolute;
  z-index: 1001;
  overflow-y: scroll;
  scrollbar-width: none;
  width: fit-content;
  max-height: 100%;
  max-width: 100%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  &::-webkit-scrollbar {
    display: none;
  }
}

.hey__modal-web-component-wrapper_with-close-btn {
  // space for the close button
  padding: 0 20px;
  max-width: calc(100% - 40px);

  &.hey__modal-web-component-wrapper_auto-width {
    padding: 0;
    max-width: 100%;
  }
}

.hey__modal-web-component-wrapper_auto-width {
  width: 100%;
}

.hey__modal-visible {
  opacity: 1;
  animation: 0.2s ease-out 0s 1 slideInFromBottom;
}

.hey__modal-hide {
  animation: 0.2s ease-out 0s 1 slideOutToBottom;
  opacity: 0;
  z-index: -1000;
}

.hey__modal-full-screen {
  top: 0 !important;
  left: 0 !important;
  height: 100%;
  width: 100% !important;
  overflow: scroll;

  ::slotted(heyflow-wrapper) {
    --heyflow-widget-height: 100%;
  }
}

.hey__modal-full-height {
  height: 100%;

  iframe {
    height: 100% !important;
  }
}

.hey__overlay {
  position: fixed;
  display: none;
  opacity: 0;
  left: 0;
  top: 0;
  background: rgba(0, 0, 0, 0.75);
  height: 100%;
  width: 100%;
  z-index: -999;
  transition: background, 0.2s;
}

.hey__overlay-visible {
  display: block;
  opacity: 1;
  z-index: 999;
}

.hey__close-modal-button {
  outline: none;
  font: inherit;
  visibility: visible;
  position: absolute;
  cursor: pointer;
  transition: top 0.2s ease 0s;
  display: flex;
  align-items: center;
  justify-content: center;
  top: 8px;
  right: 8px;
  z-index: 6;
  appearance: none;
  background: #cbcbcf;
  border: 0;
  height: 32px;
  width: 32px;
  border-radius: 50%;
  padding: 0;
  color: #56565d;

  &:hover {
    background: #27272a;
    color: #c8c8ca;
  }

  svg {
    width: 12px;
    height: 12px;
  }
}

.hey__close-modal-button_full-screen {
  top: 5px;
  right: 5px;
}

.hey__modal-full-height .hey__close-modal-button {
  top: 0;
}
`;var si=Object.defineProperty,I=(i,e,t,n)=>{for(var o=void 0,s=i.length-1,r;s>=0;s--)(r=i[s])&&(o=r(e,t,o)||o);return o&&si(e,t,o),o};const Re="heyflow-modal-element:open",ri=()=>Te("heyflow-modal-element",g),Me=class Me extends M{constructor(){super(...arguments),this.WIDGET_TAG_NAME="HEYFLOW-WRAPPER",this.bodyOverflow="",this.isFullscreen=!1,this.modalId="",this.overlayBackgroundColor="rgba(0, 0, 0, 0.6)",this.hideCloseButton=!1,this.isOpened=!1,this.areFlowStylesSet=!1,this.areFlowEventListenersSet=!1,this.doesFlowHaveWidth=!1,this.boundOnKeyDown=this.onKeyDown.bind(this),this.boundOnCustomEvent=this.onCustomEvent.bind(this),this.boundOnIframeMessage=this.onIframeMessage.bind(this)}connectedCallback(){var e;try{super.connectedCallback(),this.modalId||console.warn("Please set `modal-id`"),this.bodyOverflow=document.body.style.overflow,document.addEventListener("keydown",this.boundOnKeyDown),window.addEventListener(Re,this.boundOnCustomEvent)}catch(t){const n=(e=this.querySelector(this.WIDGET_TAG_NAME.toLowerCase()))==null?void 0:e.getAttribute("flow-id");console.warn("An error occurred while initialising modal element",{error:t,flowID:n}),C({flowID:n,message:"Error initializing modal element",error:t,source:"modal"})}}disconnectedCallback(){document.removeEventListener("keydown",this.boundOnKeyDown),window.removeEventListener("message",this.boundOnIframeMessage),window.removeEventListener(Re,this.boundOnCustomEvent),super.disconnectedCallback()}openModal(){document.body.style.overflow="hidden",this.isOpened=!0,this.setPropertiesBasedOnWidget()}closeModal(){document.body.style.overflow=this.bodyOverflow,this.isOpened=!1}setPropertiesBasedOnWidget(){var e,t,n,o;if(this.slotChild||(this.slotChild=(t=(e=this.shadowRoot)==null?void 0:e.querySelector("slot"))==null?void 0:t.assignedElements()[0]),((n=this.slotChild)==null?void 0:n.tagName)===this.WIDGET_TAG_NAME){!this.areFlowStylesSet&&!this.isFullscreen&&this.setStylesBasedOnFlow(),this.areFlowEventListenersSet||window.addEventListener("message",this.boundOnIframeMessage);const s=(o=this.slotChild)==null?void 0:o.getAttribute("style-config");let r={};if(s)try{r=JSON.parse(s)}catch(c){r={}}r.width&&(this.doesFlowHaveWidth=!0)}}onKeyDown(e){e.code==="Escape"&&this.closeModal()}onCustomEvent(e){var t;e.type===Re&&((t=e.detail)==null?void 0:t.modalId)===this.modalId&&this.openModal()}setStylesBasedOnFlow(){var o,s,r,c;this.areFlowStylesSet=!0;const{"width-mid":e,"width-wide":t}=(r=(s=(o=window.heyflow)==null?void 0:o.constants)==null?void 0:s.STYLES)!=null?r:{"width-mid":800,"width-wide":1200},n=document.createElement("style");n.innerHTML=`
			@media screen and (min-width: ${e}) {
				.hey__modal-wrapper .hey__modal-web-component-wrapper {
					top: 50%;
					left: 50%;
					right: auto;
					bottom: auto;
					transform: translate(-50%, -50%);
					max-height: 90%;
					max-width: min(${e}, 80%);
					padding: 20px;
				}
			}

			@media screen and (min-width: ${t}) {
				.hey__modal-wrapper .hey__modal-web-component-wrapper {
					max-width: min(${t}, 60%);
				}
			}
		`,(c=this.shadowRoot)==null||c.appendChild(n)}onIframeMessage(e){var n,o;if(!e.data)return;let t;try{t=JSON.parse(e.data)}catch(s){return}if(["goToScreen","goBack"].includes(t.event)&&["","true"].includes(String((n=this.slotChild)==null?void 0:n.getAttribute("scroll-up-on-navigation")))){const s=(o=this.shadowRoot)==null?void 0:o.querySelector(".hey__modal-web-component-wrapper");s&&(s.scrollTop=0)}t.event==="closeModal"&&this.closeModal()}render(){return k`
      <div
        class=${ee({"hey__modal-wrapper":!0,"hey__modal-wrapper-visible":this.isOpened})}
        style=${ut({display:this.isOpened?"block":"none"})}
      >
        <div
          class=${ee({hey__modal:!0,"hey__modal_web-component":!0,"hey__modal-visible":this.isOpened,"hey__modal-hide":!this.isOpened,"hey__modal-full-screen":this.isFullscreen})}
        >
          <div
            class=${ee({"hey__modal-web-component-wrapper":!0,"hey__modal-web-component-wrapper_auto-width":!this.doesFlowHaveWidth,"hey__modal-web-component-wrapper_with-close-btn":!this.hideCloseButton})}
          >
            <slot></slot>
            ${this.hideCloseButton?k``:k`
                  <button
                    aria-label="Close"
                    title="Close"
                    class=${ee({"hey__close-modal-button":!0,"hey__close-modal-button_full-screen":this.isFullscreen})}
                    @click="${this.closeModal}"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 12 12"
                    >
                      <path
                        fill="currentColor"
                        d="M11.747 10.535a.858.858 0 1 1-1.214 1.214L6 7.214l-4.535 4.533a.859.859 0 0 1-1.214-1.214L4.786 6 .253 1.466A.858.858 0 1 1 1.467.252L6 4.787 10.535.25a.858.858 0 1 1 1.214 1.214L7.214 6l4.533 4.535Z"
                      />
                    </svg>
                  </button>
                `}
          </div>
          <div
            class=${ee({hey__overlay:!0,"hey__overlay-visible":this.isOpened})}
            style="background-color: ${this.overlayBackgroundColor}"
            @click="${this.closeModal}"
          ></div>
        </div>
      </div>
    `}};Me.styles=ye`
    ${je(oi.toString())}
  `;let g=Me;I([m({attribute:"full-screen",type:Boolean})],g.prototype,"isFullscreen"),I([m({attribute:"modal-id",type:String})],g.prototype,"modalId"),I([m({attribute:"overlay-background-color",type:String})],g.prototype,"overlayBackgroundColor"),I([m({attribute:"hide-close-button",type:Boolean})],g.prototype,"hideCloseButton"),I([de()],g.prototype,"isOpened"),I([de()],g.prototype,"areFlowStylesSet"),I([de()],g.prototype,"areFlowEventListenersSet"),I([de()],g.prototype,"doesFlowHaveWidth");const ai=Object.freeze(Object.defineProperty({__proto__:null,ModalElement:g,default:ri},Symbol.toStringTag,{value:"Module"}));var N=[],li=function(){return N.some(function(i){return i.activeTargets.length>0})},di=function(){return N.some(function(i){return i.skippedTargets.length>0})},pt="ResizeObserver loop completed with undelivered notifications.",ci=function(){var i;typeof ErrorEvent=="function"?i=new ErrorEvent("error",{message:pt}):(i=document.createEvent("Event"),i.initEvent("error",!1,!1),i.message=pt),window.dispatchEvent(i)},te;(function(i){i.BORDER_BOX="border-box",i.CONTENT_BOX="content-box",i.DEVICE_PIXEL_CONTENT_BOX="device-pixel-content-box"})(te||(te={}));var H=function(i){return Object.freeze(i)},hi=(function(){function i(e,t){this.inlineSize=e,this.blockSize=t,H(this)}return i})(),ft=(function(){function i(e,t,n,o){return this.x=e,this.y=t,this.width=n,this.height=o,this.top=this.y,this.left=this.x,this.bottom=this.top+this.height,this.right=this.left+this.width,H(this)}return i.prototype.toJSON=function(){var e=this,t=e.x,n=e.y,o=e.top,s=e.right,r=e.bottom,c=e.left,a=e.width,l=e.height;return{x:t,y:n,top:o,right:s,bottom:r,left:c,width:a,height:l}},i.fromRect=function(e){return new i(e.x,e.y,e.width,e.height)},i})(),Ie=function(i){return i instanceof SVGElement&&"getBBox"in i},vt=function(i){if(Ie(i)){var e=i.getBBox(),t=e.width,n=e.height;return!t&&!n}var o=i,s=o.offsetWidth,r=o.offsetHeight;return!(s||r||i.getClientRects().length)},mt=function(i){var e;if(i instanceof Element)return!0;var t=(e=i==null?void 0:i.ownerDocument)===null||e===void 0?void 0:e.defaultView;return!!(t&&i instanceof t.Element)},ui=function(i){switch(i.tagName){case"INPUT":if(i.type!=="image")break;case"VIDEO":case"AUDIO":case"EMBED":case"OBJECT":case"CANVAS":case"IFRAME":case"IMG":return!0}return!1},ie=typeof window!="undefined"?window:{},ce=new WeakMap,wt=/auto|scroll/,pi=/^tb|vertical/,fi=/msie|trident/i.test(ie.navigator&&ie.navigator.userAgent),_=function(i){return parseFloat(i||"0")},V=function(i,e,t){return i===void 0&&(i=0),e===void 0&&(e=0),t===void 0&&(t=!1),new hi((t?e:i)||0,(t?i:e)||0)},gt=H({devicePixelContentBoxSize:V(),borderBoxSize:V(),contentBoxSize:V(),contentRect:new ft(0,0,0,0)}),yt=function(i,e){if(e===void 0&&(e=!1),ce.has(i)&&!e)return ce.get(i);if(vt(i))return ce.set(i,gt),gt;var t=getComputedStyle(i),n=Ie(i)&&i.ownerSVGElement&&i.getBBox(),o=!fi&&t.boxSizing==="border-box",s=pi.test(t.writingMode||""),r=!n&&wt.test(t.overflowY||""),c=!n&&wt.test(t.overflowX||""),a=n?0:_(t.paddingTop),l=n?0:_(t.paddingRight),h=n?0:_(t.paddingBottom),d=n?0:_(t.paddingLeft),u=n?0:_(t.borderTopWidth),p=n?0:_(t.borderRightWidth),E=n?0:_(t.borderBottomWidth),w=n?0:_(t.borderLeftWidth),x=d+l,G=a+h,D=w+p,F=u+E,O=c?i.offsetHeight-F-i.clientHeight:0,fe=r?i.offsetWidth-D-i.clientWidth:0,Ne=o?x+D:0,He=o?G+F:0,J=n?n.width:_(t.width)-Ne-fe,ve=n?n.height:_(t.height)-He-O,Hi=J+x+fe+D,Di=ve+G+O+F,Rt=H({devicePixelContentBoxSize:V(Math.round(J*devicePixelRatio),Math.round(ve*devicePixelRatio),s),borderBoxSize:V(Hi,Di,s),contentBoxSize:V(J,ve,s),contentRect:new ft(d,a,J,ve)});return ce.set(i,Rt),Rt},bt=function(i,e,t){var n=yt(i,t),o=n.borderBoxSize,s=n.contentBoxSize,r=n.devicePixelContentBoxSize;switch(e){case te.DEVICE_PIXEL_CONTENT_BOX:return r;case te.BORDER_BOX:return o;default:return s}},vi=(function(){function i(e){var t=yt(e);this.target=e,this.contentRect=t.contentRect,this.borderBoxSize=H([t.borderBoxSize]),this.contentBoxSize=H([t.contentBoxSize]),this.devicePixelContentBoxSize=H([t.devicePixelContentBoxSize])}return i})(),_t=function(i){if(vt(i))return 1/0;for(var e=0,t=i.parentNode;t;)e+=1,t=t.parentNode;return e},mi=function(){var i=1/0,e=[];N.forEach(function(r){if(r.activeTargets.length!==0){var c=[];r.activeTargets.forEach(function(l){var h=new vi(l.target),d=_t(l.target);c.push(h),l.lastReportedSize=bt(l.target,l.observedBox),d<i&&(i=d)}),e.push(function(){r.callback.call(r.observer,c,r.observer)}),r.activeTargets.splice(0,r.activeTargets.length)}});for(var t=0,n=e;t<n.length;t++){var o=n[t];o()}return i},$t=function(i){N.forEach(function(t){t.activeTargets.splice(0,t.activeTargets.length),t.skippedTargets.splice(0,t.skippedTargets.length),t.observationTargets.forEach(function(o){o.isActive()&&(_t(o.target)>i?t.activeTargets.push(o):t.skippedTargets.push(o))})})},wi=function(){var i=0;for($t(i);li();)i=mi(),$t(i);return di()&&ci(),i>0},ze,Et=[],gi=function(){return Et.splice(0).forEach(function(i){return i()})},yi=function(i){if(!ze){var e=0,t=document.createTextNode(""),n={characterData:!0};new MutationObserver(function(){return gi()}).observe(t,n),ze=function(){t.textContent="".concat(e?e--:e++)}}Et.push(i),ze()},bi=function(i){yi(function(){requestAnimationFrame(i)})},he=0,_i=function(){return!!he},$i=250,Ei={attributes:!0,characterData:!0,childList:!0,subtree:!0},St=["resize","load","transitionend","animationend","animationstart","animationiteration","keyup","keydown","mouseup","mousedown","mouseover","mouseout","blur","focus"],At=function(i){return i===void 0&&(i=0),Date.now()+i},Pe=!1,Si=(function(){function i(){var e=this;this.stopped=!0,this.listener=function(){return e.schedule()}}return i.prototype.run=function(e){var t=this;if(e===void 0&&(e=$i),!Pe){Pe=!0;var n=At(e);bi(function(){var o=!1;try{o=wi()}finally{if(Pe=!1,e=n-At(),!_i())return;o?t.run(1e3):e>0?t.run(e):t.start()}})}},i.prototype.schedule=function(){this.stop(),this.run()},i.prototype.observe=function(){var e=this,t=function(){return e.observer&&e.observer.observe(document.body,Ei)};document.body?t():ie.addEventListener("DOMContentLoaded",t)},i.prototype.start=function(){var e=this;this.stopped&&(this.stopped=!1,this.observer=new MutationObserver(this.listener),this.observe(),St.forEach(function(t){return ie.addEventListener(t,e.listener,!0)}))},i.prototype.stop=function(){var e=this;this.stopped||(this.observer&&this.observer.disconnect(),St.forEach(function(t){return ie.removeEventListener(t,e.listener,!0)}),this.stopped=!0)},i})(),Be=new Si,xt=function(i){!he&&i>0&&Be.start(),he+=i,!he&&Be.stop()},Ai=function(i){return!Ie(i)&&!ui(i)&&getComputedStyle(i).display==="inline"},xi=(function(){function i(e,t){this.target=e,this.observedBox=t||te.CONTENT_BOX,this.lastReportedSize={inlineSize:0,blockSize:0}}return i.prototype.isActive=function(){var e=bt(this.target,this.observedBox,!0);return Ai(this.target)&&(this.lastReportedSize=e),this.lastReportedSize.inlineSize!==e.inlineSize||this.lastReportedSize.blockSize!==e.blockSize},i})(),Oi=(function(){function i(e,t){this.activeTargets=[],this.skippedTargets=[],this.observationTargets=[],this.observer=e,this.callback=t}return i})(),ue=new WeakMap,Ot=function(i,e){for(var t=0;t<i.length;t+=1)if(i[t].target===e)return t;return-1},pe=(function(){function i(){}return i.connect=function(e,t){var n=new Oi(e,t);ue.set(e,n)},i.observe=function(e,t,n){var o=ue.get(e),s=o.observationTargets.length===0;Ot(o.observationTargets,t)<0&&(s&&N.push(o),o.observationTargets.push(new xi(t,n&&n.box)),xt(1),Be.schedule())},i.unobserve=function(e,t){var n=ue.get(e),o=Ot(n.observationTargets,t),s=n.observationTargets.length===1;o>=0&&(s&&N.splice(N.indexOf(n),1),n.observationTargets.splice(o,1),xt(-1))},i.disconnect=function(e){var t=this,n=ue.get(e);n.observationTargets.slice().forEach(function(o){return t.unobserve(e,o.target)}),n.activeTargets.splice(0,n.activeTargets.length)},i})(),Ci=(function(){function i(e){if(arguments.length===0)throw new TypeError("Failed to construct 'ResizeObserver': 1 argument required, but only 0 present.");if(typeof e!="function")throw new TypeError("Failed to construct 'ResizeObserver': The callback provided as parameter 1 is not a function.");pe.connect(this,e)}return i.prototype.observe=function(e,t){if(arguments.length===0)throw new TypeError("Failed to execute 'observe' on 'ResizeObserver': 1 argument required, but only 0 present.");if(!mt(e))throw new TypeError("Failed to execute 'observe' on 'ResizeObserver': parameter 1 is not of type 'Element");pe.observe(this,e,t)},i.prototype.unobserve=function(e){if(arguments.length===0)throw new TypeError("Failed to execute 'unobserve' on 'ResizeObserver': 1 argument required, but only 0 present.");if(!mt(e))throw new TypeError("Failed to execute 'unobserve' on 'ResizeObserver': parameter 1 is not of type 'Element");pe.unobserve(this,e)},i.prototype.disconnect=function(){pe.disconnect(this)},i.toString=function(){return"function ResizeObserver () { [polyfill code] }"},i})();class Ti{constructor(){this.queue=[],this.acquired=!1,this.currentOwner=null}createAndSetOwnerToken(){const e=Symbol("ResourceLockToken");return this.currentOwner=e,e}async acquire(){return this.acquired?new Promise((e,t)=>{this.queue.push(()=>{e(this.createAndSetOwnerToken())})}):(this.acquired=!0,this.createAndSetOwnerToken())}async release(e,t){if(this.currentOwner!==e){console.warn("Attempted to release ResourceLock without valid ownership token",t?`(embed: ${t})`:"");return}if(this.currentOwner=null,this.queue.length===0){this.acquired=!1;return}const n=this.queue.shift();if(n!==void 0)return new Promise(o=>{n(),o()})}}class Ct{static set(e,t){try{window.localStorage.setItem(e,t)}catch(n){console.warn("Failed to write to localStorage:",n)}}static get(e){try{return window.localStorage.getItem(e)}catch(t){return console.warn("Failed to read from localStorage:",t),null}}}const ki=i=>{const e={"x-is-heyflow-embed":"true"},t=Ct.get(`heyflow-variant-${i}`);return t!==null&&(e["x-heyflow-variant"]=t),e},Ri=async i=>{const e=Pi(i);console.log("flowSrc ",e);const t=await fetch(e,{headers:ki(i)}),n=t.headers.get("x-heyflow-variant");if(n!==null&&Ct.set(`heyflow-variant-${i}`,n),!t.ok){const o=`Error while fetching Flow: ${t.status}`;throw new Error(o)}return t.text()},{VITE_FLOW_URL_PATTERN:Ii}=We,zi="[FLOW_ID]",Pi=i=>Ii.replace(zi,i);var Bi=Object.defineProperty,z=(i,e,t,n)=>{for(var o=void 0,s=i.length-1,r;s>=0;s--)(r=i[s])&&(o=r(e,t,o)||o);return o&&Bi(e,t,o),o};const Tt=new Ti,Li=()=>Te("heyflow-wrapper",kt),Mi=.01,A=($=class extends M{constructor(){super(...arguments),this.scriptQueue=[],this.embedIndex=0,this.embedReference="",this.boundOnLessCompiled=this.onLessCompiled.bind(this),this.boundOnIframeMessage=this.onIframeMessage.bind(this),this.template=$.loadingTemplate,this.dynamicHeight=!1,this.urlParams="",this.scrollUpOnNavigation=!1,this.lang=navigator.language,this.getSafeNumber=e=>e&&!isNaN(e)?e:0}getHeyflowWindowContext(){var e;return(e=window.heyflow)==null?void 0:e[this.embedReference]}releaseOwnLock(){if(!this.lockToken)return;const e=this.lockToken;return this.lockToken=void 0,Tt.release(e,this.embedReference)}setWidthOverrides(){var s,r,c,a,l,h;const{"width-narrow":e,"width-mid":t,"width-wide":n}=(h=(l=(r=(s=window.heyflow)==null?void 0:s.constants)==null?void 0:r.STYLES)!=null?l:(a=(c=this.getHeyflowWindowContext())==null?void 0:c.constants)==null?void 0:a.STYLES)!=null?h:{};Object.entries({"width-narrow":e,"width-mid":t,"width-wide":n}).forEach(([d,u])=>{document.documentElement.style.setProperty(`--heyflow-widget-${d}`,u)})}getStyleConfig(){var t;return!this.dynamicHeight&&((t=this.styleConfig)==null?void 0:t.height)!==void 0?S({overflow:"auto"},this.styleConfig):!!this.closest("heyflow-modal-element")&&this.styleConfig.width==="100%"?W(S({},this.styleConfig),{width:"100vw"}):this.styleConfig}render(){return k`
      <article
        class="heyflow-widget-root"
        style=${ut(S({},this.getStyleConfig()))}
        lang="${this.lang}"
      >
        ${this.template}
      </article>
    `}async connectedCallback(){var e;this.lockToken=await Tt.acquire(),window.embeds=(e=window.embeds)!=null?e:new Set;try{if(!this.isConnected||(super.connectedCallback(),!this.flowId)||(this.setupEmbedReference(),await this.updateTemplateWithFlow(),!this.isConnected))return;this.detectIFrameEnvironment(),this.setupEventListeners(),this.injectFontDefinitions(),this.initFlow(),this.setupResizeObserver()}catch(t){this.isConnected&&(console.warn("An error occurred while initialising a heyflow widget",{error:t,flowId:this.flowId,embedIndex:this.embedIndex}),(t==null?void 0:t.message)!=="Error while fetching Flow: 404"&&C({flowID:this.flowId,message:"Error initializing heyflow-wrapper",error:t,embedIndex:this.embedIndex,source:"embed"}))}finally{const t=this.releaseOwnLock();t&&await t}}disconnectedCallback(){var e,t;this.releaseOwnLock(),window.removeEventListener("lessCompiled",this.boundOnLessCompiled),window.removeEventListener("message",this.boundOnIframeMessage),window.embeds.delete(this.embedReference),(t=(e=this.getHeyflowWindowContext())==null?void 0:e.cleanupTracking)==null||t.call(e)}detectIFrameEnvironment(){var e,t;window.top!==window.self&&((t=(e=this.shadowRoot)==null?void 0:e.querySelector("article"))==null||t.classList.add("parent-is-iframe"))}setupEmbedReference(){document.querySelectorAll("heyflow-wrapper").length!==1&&(this.embedIndex=window.embeds.size),this.embedReference=`${this.flowId}-${this.embedIndex}`,window.embeds.add(this.embedReference),this.setAttribute("index",this.embedReference)}async updateTemplateWithFlow(){var t;const e=Pt(await Ri(this.flowId));this.flow=Bt(e,this.flowId,this.embedReference);try{await this.injectFlowStyles(),this.enqueueScripts(),await this.injectScripts()}catch(n){throw C({flowID:this.flowId,message:"Error injecting assets while initialising widget",error:n,embedIndex:this.embedIndex,source:"embed"}),n}this.template=(t=k`${this.flow.body}`)!=null?t:$.fallbackTemplate,await this.updateComplete}async injectFlowStyles(){return new Promise(e=>{var a,l,h;let t=!1,n=(a=this.flow)==null?void 0:a.head.querySelector("style#less\\:static-flow-src-style");if(!n){const d=(l=this.flow)==null?void 0:l.head.querySelectorAll("style");n=d==null?void 0:d[(d==null?void 0:d.length)-1]}const o=(h=this.flow)==null?void 0:h.head.querySelectorAll('link[rel="stylesheet"]'),s=d=>{var u;try{(u=this.shadowRoot)==null||u.appendChild(d)}catch(p){throw C({flowID:this.flowId,message:"Error appending style related node to shadowRoot",error:p,embedIndex:this.embedIndex,source:"embed"}),p}},r=d=>()=>{clearTimeout(d),e()},c=d=>(u,p,E,w,x)=>{clearTimeout(d),x&&C({flowID:this.flowId,message:"Error loading stylesheet",error:x,embedIndex:this.embedIndex,source:"embed"})};n&&(n.innerHTML=n.innerHTML.replace(/:root/g,":host").replace(/(\d)(rem)/g,"$1em"),s(n)),o==null||o.forEach(d=>{const u=d.href.split("/").pop();if(u!=null&&u.match(/app(?:-.+|)\.css/)||u!=null&&u.match(/flow(?:-.+|)\.css/)){const p=document.createElement("link"),E=u.replace("flow","app");p.href=`${d.href.replace(u,E)}?q=${this.embedReference}`,p.rel=d.rel,t=!0;const w=setTimeout(()=>{ne({flowID:this.flowId,message:"Stylesheet has not been loaded after 5000ms",data:{filename:u},embedIndex:this.embedIndex,source:"embed"})},5e3);p.onload=r(w),p.onerror=c(w),s(p),d.remove()}}),(!n&&!(o!=null&&o.length)||!t)&&e()})}enqueueScripts(){if(this.flow){const e=De("script",this.flow.head);this.scriptQueue=e}}async injectScripts(){return new Promise(e=>{const t=this.scriptQueue.filter(a=>!!a.src),n=t.filter(a=>a.getAttribute("data-is-heyflow-script")==="true"),o=n.length>0,s=o?n:t;let r=0;function c(a){o&&a.getAttribute("data-is-heyflow-script")!=="true"||(r++,r===s.length&&e())}this.scriptQueue.forEach(a=>{var h;const l=document.createElement("script");a.src?(l.src=a.src,l.type=a.type,l.onload=()=>c(a),l.onerror=()=>{console.warn(`failed to inject script from: ${l.src}, please disable your ad-blocker`)}):l.innerHTML=a.innerHTML,a.src.match(/(app|flow|custom-code)(?:-.+|)\.js/)&&a.type==="module"&&(l.src=`${a.src}?q=${this.embedReference}`),(h=this.shadowRoot)==null||h.appendChild(l)}),s.length===0&&e()})}injectFontDefinitions(){this.flow&&De('link[as="style"]:not([data-is-heyflow-style])',this.flow.head).forEach(t=>{const n=document.createElement("link");n.rel="stylesheet",n.href=t.href,document.head.appendChild(n)})}onLessCompiled(){var t;const e=document.getElementById("less:static-flow-src-style");e&&((t=this.shadowRoot)==null||t.appendChild(e))}onIframeMessage(e){var n;if(!e.data)return;let t;try{t=JSON.parse(e.data)}catch(o){return}if(["goToScreen","goBack"].includes(t.event)&&this.scrollUpOnNavigation){const o=document.querySelector(`[index="${t.widgetWrapperRef}"]`),s=(n=o==null?void 0:o.shadowRoot)==null?void 0:n.querySelector('[data-id="heyflow-main"]');this.dynamicHeight?o==null||o.scrollIntoView():s&&(s.scrollTop=0,s.scrollIntoView())}}setupEventListeners(){window.addEventListener("lessCompiled",this.boundOnLessCompiled),window.addEventListener("message",this.boundOnIframeMessage)}initFlow(){var e,t,n;if(this.setWidthOverrides(),document.dispatchEvent(new CustomEvent("finishedInjection",{detail:{urlParams:this.urlParams,embedReference:this.embedReference}})),this.screen)if((e=window.heyflow)!=null&&e.setAlternativeInitialScreen)window.heyflow.setAlternativeInitialScreen(this.screen,!0);else if((t=this.getHeyflowWindowContext())!=null&&t.setAlternativeInitialScreen)(n=this.getHeyflowWindowContext())==null||n.setAlternativeInitialScreen(this.screen,!0);else return;delete window.currentlyMounting}loadResizeObserver(){return window.ResizeObserver?window.ResizeObserver:Ci}setupResizeObserver(){var o;const e=this.loadResizeObserver(),t=new e(s=>{const r=s[0].borderBoxSize[0].blockSize;this.handleDynamicSizing(Math.ceil(r))}),n=(o=this.shadowRoot)==null?void 0:o.querySelector("form");n&&t.observe(n)}handleDynamicSizing(e){var t,n,o,s,r,c,a,l,h,d,u,p,E,w;if(this.dynamicHeight){const x=(t=this.shadowRoot)==null?void 0:t.querySelector("form + div"),G=(n=this.shadowRoot)==null?void 0:n.querySelector("form"),D=(o=this.shadowRoot)==null?void 0:o.querySelector("header"),F=(s=this.shadowRoot)==null?void 0:s.querySelector(".footer-container"),O=(r=this.shadowRoot)==null?void 0:r.querySelector(".heyflow-widget-root"),fe=this.getSafeNumber(parseInt((a=(c=O==null?void 0:O.style)==null?void 0:c.borderTopWidth)!=null?a:"0",10)+parseInt((h=(l=O==null?void 0:O.style)==null?void 0:l.borderBottomWidth)!=null?h:"0",10)),Ne=G?this.getSafeNumber(parseInt((d=getComputedStyle(G).marginTop)!=null?d:0)+parseInt((u=getComputedStyle(G).marginBottom)!=null?u:0)):0,He=Math.floor(e*Mi),J=((p=D==null?void 0:D.clientHeight)!=null?p:0)+((E=F==null?void 0:F.clientHeight)!=null?E:0)+((w=x==null?void 0:x.clientHeight)!=null?w:0)+e+fe+Ne+He;this.styleConfig=W(S({},this.styleConfig),{height:`${J}px`})}}},$.fallbackTemplate=k`<p>
    🤕 Error integrating Heyflow, check javascript console for details!
  </p>`,$.loadingTemplate=k`<loader-element />`,$.styles=ye`
    :host {
      all: initial;
      width: 100%;
    }

    /*Workaround to make Material Icons Work https://github.com/google/material-design-icons/issues/1165*/
    .material-icons {
      font-family: 'Material Icons';
      font-style: normal;
    }

    .heyflow-widget-root {
      margin: 0 auto;
      // We set --heyflow-widget-height in modal-element if needed
      height: var(--heyflow-widget-height, 600px);
      max-width: 100%;
    }

    /* TODO these are hacky overrides to fix sizing issues if the web component is embedded inside of an iframe.
		The iframe class is set only if the web component is running inside of an iframe.*/
    .parent-is-iframe .multiple-choice .option-content.picture {
      height: auto;
    }

    /* This prevents weird whitespace problem under large images. */
    .parent-is-iframe .block-content.image-block {
      display: flex;
    }

    .parent-is-iframe img {
      /* overrides an inline style. */
      height: auto !important;
      max-height: 100%;
    }

    /* adds an overflow hidden to the span in the button cause it shows scroll bars in Safari and this would break the button */
    .generic-button-block .content .label,
    .generic-button-block .content .line2 {
      overflow: hidden;
    }

    /* !importants are here because of packages/flow/src/style/x_responsive.less */
    form section > .block > .inner-wide {
      width: min(var(--heyflow-widget-width-wide), 100%) !important;
    }

    form section > .block > .inner-mid {
      width: min(var(--heyflow-widget-width-mid), 100%) !important;
    }

    form section > .block > .inner-narrow {
      width: min(var(--heyflow-widget-width-narrow), 100%) !important;
    }
  `,$);z([m()],A.prototype,"template"),z([m({attribute:"flow-id"})],A.prototype,"flowId"),z([m({attribute:"screen"})],A.prototype,"screen"),z([m({attribute:"style-config",type:Object})],A.prototype,"styleConfig"),z([m({attribute:"dynamic-height",type:Boolean})],A.prototype,"dynamicHeight"),z([m({attribute:"url-parameters"})],A.prototype,"urlParams"),z([m({attribute:"scroll-up-on-navigation",type:Boolean})],A.prototype,"scrollUpOnNavigation"),z([m({attribute:"lang"})],A.prototype,"lang");let kt=A;const Ni=Object.freeze(Object.defineProperty({__proto__:null,HeyflowWrapper:kt,default:Li},Symbol.toStringTag,{value:"Module"}))})();
})()