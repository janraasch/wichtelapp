/* esm.sh - @zachleat/snow-fall@1.0.3 */
var g=Object.create;var f=Object.defineProperty;var w=Object.getOwnPropertyDescriptor;var S=Object.getOwnPropertyNames;var b=Object.getPrototypeOf,v=Object.prototype.hasOwnProperty;var C=(t,e)=>()=>(e||t((e={exports:{}}).exports,e),e.exports);var E=(t,e,s,l)=>{if(e&&typeof e=="object"||typeof e=="function")for(let o of S(e))!v.call(t,o)&&o!==s&&f(t,o,{get:()=>e[o],enumerable:!(l=w(e,o))||l.enumerable});return t};var j=(t,e,s)=>(s=t!=null?g(b(t)):{},E(e||!t||!t.__esModule?f(s,"default",{value:t,enumerable:!0}):s,t));var p=C(()=>{var h=class t extends HTMLElement{static random(e,s){return e+Math.floor(Math.random()*(s-e)+1)}static attrs={count:"count",mode:"mode",text:"text"};generateCss(e,s){let l=[];l.push(`
    :host([mode="element"]) {
        display: block;
        position: relative;
        overflow: hidden;
    }
    :host([mode="page"]) {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
    }
    :host([mode="page"]),
    :host([mode="element"]) > * {
        pointer-events: none;
    }
    :host([mode="element"]) ::slotted(*) {
        pointer-events: all;
    }
    * {
        position: absolute;
    }
    :host([text]) * {
        font-size: var(--snow-fall-size, 1em);
    }
    :host(:not([text])) * {
        width: var(--snow-fall-size, 10px);
        height: var(--snow-fall-size, 10px);
        background: var(--snow-fall-color, rgba(255,255,255,.5));
        border-radius: 50%;
    }
    `);let o={width:100,height:100},n={x:"vw",y:"vh"};e==="element"&&(o={width:this.firstElementChild.clientWidth,height:this.firstElementChild.clientHeight},n={x:"px",y:"px"});for(let a=1;a<=s;a++){let i=t.random(1,100)*o.width/100,r=t.random(-10,10)*o.width/100,c=Math.round(t.random(30,100)),u=c*o.height/100,x=o.height,d=t.random(1,1e4)*1e-4,$=t.random(10,30),y=t.random(0,30)*-1;l.push(`
    :nth-child(${a}) {
        opacity: ${t.random(0,1e3)*.001};
        transform: translate(${i}${n.x}, -10px) scale(${d});
        animation: fall-${a} ${$}s ${y}s linear infinite;
    }
    
    @keyframes fall-${a} {
        ${c}% {
            transform: translate(${i+r}${n.x}, ${u}${n.y}) scale(${d});
        }
    
        to {
            transform: translate(${i+r/2}${n.x}, ${x}${n.y}) scale(${d});
        }
    }`)}return l.join(`
    `)}connectedCallback(){if(this.shadowRoot||!("replaceSync"in CSSStyleSheet.prototype))return;let e=parseInt(this.getAttribute(t.attrs.count))||100,s;this.hasAttribute(t.attrs.mode)?s=this.getAttribute(t.attrs.mode):(s=this.firstElementChild?"element":"page",this.setAttribute(t.attrs.mode,s));let l=new CSSStyleSheet;l.replaceSync(this.generateCss(s,e));let o=this.attachShadow({mode:"open"});o.adoptedStyleSheets=[l];let n=document.createElement("div"),a=this.getAttribute(t.attrs.text);n.innerText=a||"";for(let i=0,r=e;i<r;i++)o.appendChild(n.cloneNode(!0));o.appendChild(document.createElement("slot"))}};customElements.define("snow-fall",h)});var m=j(p()),M=m.default??m;export{M as default};
    //# sourceMappingURL=snow-fall.mjs.map
