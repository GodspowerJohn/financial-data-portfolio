(() => {
  'use strict';
  const cfg = window.PORTFOLIO_CONFIG || {};
  const data = window.PORTFOLIO_DATA || {settlements:[],commissions:[]};
  const $=id=>document.getElementById(id);
  const n=v=>Number(v)||0;
  const sum=(rows,key)=>rows.reduce((acc,row)=>acc+n(row[key]),0);
  const fmtN=x=>Math.round(x).toLocaleString('en-NG');
  const money=x=> {let v=Math.abs(x);return '₦'+(v>=1e6?(v/1e6).toFixed(v>=10e6?1:2)+'m':v>=1e3?(v/1e3).toFixed(1)+'k':Math.round(v).toLocaleString('en-NG'));};
  const pct=x=>Number.isFinite(x)?(x*100).toFixed(1)+'%':'n/a';
  const monthName=x=>({ '05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct'})[x.slice(5)]||x;
  const settlementGap=r=>r.reconciliation_status==='Matched'?0:Math.abs(n(r.expected_settlement_ngn)-n(r.bank_settlement_ngn));
  const total=data.settlements.length;
  const matched=data.settlements.filter(x=>x.reconciliation_status==='Matched').length;
  if ($('heroTx'))$('heroTx').textContent=fmtN(total);
  if ($('heroMatch'))$('heroMatch').textContent=pct(matched/(total||1));
  if ($('heroGap'))$('heroGap').textContent=money(data.settlements.reduce((s,r)=>s+settlementGap(r),0));
  if ($('year'))$('year').textContent=String(new Date().getFullYear());
  // Only show genuine contact links provided by the portfolio owner.
  const contacts=[['Email',cfg.email?'mailto:'+cfg.email:''],['GitHub',cfg.github],['LinkedIn',cfg.linkedin],['Résumé',cfg.resume]];
  const contact= $('contact-links');
  if (contact){
    contacts.filter(x=>x[1]).forEach(([label,href])=> {const a=document.createElement('a'); a.textContent=label+' ↗';a.href=href;if(!href.startsWith('mailto:')){a.target='_blank';a.rel='noopener noreferrer'} contact.appendChild(a);});
    if(contact.children.length){$('contact-note').textContent='Let’s discuss data, financial reporting and operational insight.';} 
  }
  let active='settlement';
  const opt=$('demo-filter');
  const render=()=>{
    if(!opt)return;
    const isS=active==='settlement';
    const groupOptions = isS?['All', 'Paystack','Monnify','Interswitch','Flutterwave']:['All','Sportsbook','Elbet','Globalbet','Goldenrace'];
    const current=opt.value;
    opt.replaceChildren();
    groupOptions.forEach(value=>{const el=document.createElement('option');el.value=value;el.textContent=value==='All'?isS?'All providers':'All products':value;opt.appendChild(el);});
    if(groupOptions.includes(current))opt.value=current;
    $('filter-label').textContent=isS?'Provider':'Product';
    opt.setAttribute('aria-label',isS?'Provider':'Product');
    $('tab-settlement').setAttribute('aria-selected',String(isS));
    $('tab-commission').setAttribute('aria-selected',String(!isS));
    const rows=(isS?data.settlements:data.commissions).filter(r=>opt.value==='All'||r[isS?'provider':'product']===opt.value);
    const kpis=[];
    if(isS){
      const match=rows.filter(r=>r.reconciliation_status==='Matched').length;
      const expected=sum(rows,'expected_settlement_ngn');
      const gap=rows.reduce((v,r)=>v+settlementGap(r),0);
      const late=rows.filter(r=>n(r.settlement_delay_hours)>48).length;
      kpis.push(['Transactions assessed',fmtN(rows.length)],['Financial match rate',pct(match/(rows.length||1))],['Unreconciled exposure',money(gap)],['Delayed >48h',fmtN(late)]);
      $('demo-insight').innerHTML=`<strong>What this tells an operations team:</strong> ${fmtN(rows.length-match)} transaction records need amount-level review. The estimated absolute reconciliation exposure is ${money(gap)}. Time-based exceptions are tracked separately to avoid confusing settlement speed with financial accuracy.`;
    }else{
      const ggr=sum(rows,'ggr_ngn'),totalComm=sum(rows,'total_commission_ngn');
      const atRisk=rows.filter(r=>r.ggr_ngn<=0||r.total_commission_ngn/r.ggr_ngn>.40).length;
      kpis.push(['Total stake',money(sum(rows,'stake_ngn'))],['Gross gaming revenue',money(ggr)],['Commission / GGR',ggr>0?pct(totalComm/ggr):'n/a'],['Rows above risk threshold',fmtN(atRisk)]);
      $('demo-insight').innerHTML=`<strong>What this tells a finance team:</strong> ${fmtN(atRisk)} agent-product-month observations breach the illustrative 40% cost-of-GGR threshold or record non-positive GGR. These merit investigation, not automatic enforcement. Negative GGR rows are not used as denominators.`;
    }
    const k=$('kpi-row');k.replaceChildren();kpis.forEach(([label,value])=>{const el=document.createElement('div');el.className='kpi';const a=document.createElement('div');a.className='kpi-label';a.textContent=label;const b=document.createElement('div');b.className='kpi-value';b.textContent=value;el.append(a,b);k.appendChild(el);});
    const mths=['2026-05','2026-06','2026-07','2026-08','2026-09','2026-10'];
    const points=mths.map(month=>{
      const rs=rows.filter(r=>r.month===month);
      if(isS){return {month, value:rs.length?rs.filter(r=>r.reconciliation_status==='Matched').length/rs.length:0,label:pct(rs.length?rs.filter(r=>r.reconciliation_status==='Matched').length/rs.length:0)};}
      const gg=sum(rs,'ggr_ngn');const cc=sum(rs,'total_commission_ngn');return {month,value:gg>0?cc/gg:0,label:gg>0?pct(cc/gg):'n/a'};
    });
    $('chart-title').textContent=isS?'Financial match rate over time':'Commission cost relative to GGR';
    $('chart-note').textContent=isS?'Percent of transactions matched, by month':'Monthly ratio based on total commission / total GGR';
    const maxVal=isS?1:Math.max(.5,...points.map(x=>x.value));
    const chart=$('demo-chart');chart.replaceChildren();
    points.forEach(d=>{const col=document.createElement('div');col.className='bar-col';const bar=document.createElement('div');bar.className='bar';bar.style.height=Math.max(2, d.value/maxVal*95)+'%';bar.setAttribute('tabindex','0');bar.setAttribute('aria-label',monthName(d.month)+' '+d.label);const tip=document.createElement('span');tip.textContent=d.label;bar.appendChild(tip);const lbl=document.createElement('span');lbl.textContent=monthName(d.month);col.append(bar,lbl);chart.appendChild(col);});
    $('breakdown-title').textContent=isS?'Provider split':'Product split';
    $('breakdown-note').textContent=isS?'Share of transactions in filtered data':'Share of stakes in filtered data';
    const groups=isS?['Paystack','Monnify','Interswitch','Flutterwave']:['Sportsbook','Elbet','Globalbet','Goldenrace'];
    const field=isS?'provider':'product';const denominator=isS?rows.length:sum(rows,'stake_ngn');
    const breakdown=$('demo-breakdown');breakdown.replaceChildren();
    groups.forEach(g=>{
      const filtered=rows.filter(x=>x[field]===g);
      const share=isS?filtered.length/(denominator||1):sum(filtered,'stake_ngn')/(denominator||1);
      const el=document.createElement('div');el.className='breakdown-row';const la=document.createElement('span');la.className='breakdown-label';la.textContent=g;const v=document.createElement('span');v.className='breakdown-val';v.textContent=pct(share);const track=document.createElement('div');track.className='track';const fill=document.createElement('div');fill.style.width=Math.min(100,share*100)+'%';track.appendChild(fill);el.append(la,v,track);breakdown.appendChild(el);
    });
  };
  $('tab-settlement')?.addEventListener('click',()=>{active='settlement';opt.value='All';render();});
  $('tab-commission')?.addEventListener('click',()=>{active='commission';opt.value='All';render();});
  opt?.addEventListener('change',render);
  render();
})();
