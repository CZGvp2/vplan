<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html"/>

<xsl:attribute-set name="ankerklasse">
  <xsl:attribute name="name">
    <xsl:value-of select="'Kl'"/> 
    <xsl:value-of select="translate(kl_kurz,'äöüÄÖÜßáéíóúý','aouAOUsaeiouy')"/>
  </xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="ankerlehrer">
  <xsl:attribute name="name">
    <xsl:value-of select="'Le'"/> 
    <xsl:value-of select="translate(le_kurz,'äöüÄÖÜßáéíóúý','aouAOUsaeiouy')"/>
  </xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="ankerraum">
  <xsl:attribute name="name">
    <xsl:value-of select="'Ra'"/> 
    <xsl:value-of select="translate(ra_kurz,'äöüÄÖÜßáéíóúý','aouAOUsaeiouy')"/>
  </xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="ankerstunde">
  <xsl:attribute name="name">
    <xsl:value-of select="'St'"/> 
    <xsl:value-of select="."/>
  </xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="linkklasse">
  <xsl:attribute name="href">
    <xsl:value-of select="'#Kl'"/> 
    <xsl:value-of select="translate(kl_kurz,'äöüÄÖÜßáéíóúý','aouAOUsaeiouy')"/>
  </xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="linklehrer">
  <xsl:attribute name="href">
    <xsl:value-of select="'#Le'"/> 
    <xsl:value-of select="translate(le_kurz,'äöüÄÖÜßáéíóúý','aouAOUsaeiouy')"/>
  </xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="linkraum">
  <xsl:attribute name="href">
    <xsl:value-of select="'#Ra'"/> 
    <xsl:value-of select="translate(ra_kurz,'äöüÄÖÜßáéíóúý','aouAOUsaeiouy')"/>
  </xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="linkstunde">
  <xsl:attribute name="href">
    <xsl:value-of select="'#St'"/> 
    <xsl:value-of select="."/>
  </xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="linkplanle">
  <xsl:attribute name="href">
    <xsl:value-of select="'#Le'"/> 
    <xsl:value-of select="translate(.,'äöüÄÖÜßáéíóúý','aouAOUsaeiouy')"/>
  </xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="linkplankl">
  <xsl:attribute name="href">
    <xsl:value-of select="'#Kl'"/> 
    <xsl:value-of select="translate(.,'äöüÄÖÜßáéíóúý','aouAOUsaeiouy')"/>
  </xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="linkplanra">
  <xsl:attribute name="href">
    <xsl:value-of select="'#Ra'"/> 
    <xsl:value-of select="translate(.,'äöüÄÖÜßáéíóúý','aouAOUsaeiouy')"/>
  </xsl:attribute>
</xsl:attribute-set>

<xsl:template match="/sp">  
  <html>
  <head>
    <link rel="stylesheet" type="text/css" href="splan.css" />
    <title>Stundenplan</title>
  </head>
  <body>
<H5> </H5><H3> </H3>    <a name="anfang"></a>
    <xsl:call-template name="hauptmenu"/>
  </body>
  </html>
</xsl:template>

<xsl:template name="hauptmenu"> 
  <div class="hauptmenudatum"><xsl:value-of select="/sp/kopf/datum"/></div>
  <div class="spschulname"><xsl:value-of select="/sp/kopf/schulname"/></div>
  <br/>
  <div class="hauptmenunach">nach Stunden:</div>
  <xsl:call-template name="menustunde" />
  <div class="clear"/>
  <br/>
  <div class="hauptmenunach">nach Klassen:</div>
  <xsl:call-template name="menuklasse" />
  <div class="clear"/>
  <br/>
  <div class="hauptmenunach">nach Lehrern:</div>
  <xsl:call-template name="menulehrer" />
  <div class="clear"/>
  <br/>
  <div class="hauptmenunach">nach Räumen:</div>
  <xsl:call-template name="menuraum" />
  <div class="clear"/>
  <xsl:for-each select="/sp/zeitraster/zr_stunde">
    <xsl:call-template name="kopfstunde" />
    <xsl:call-template name="einzelplanstunde" />
  </xsl:for-each>
  <xsl:for-each select="/sp/klassen/kl">
    <xsl:call-template name="kopfklasse" />
    <xsl:call-template name="einzelplanklasse" />
  </xsl:for-each>
  <xsl:for-each select="/sp/lehrer/le">
    <xsl:call-template name="kopflehrer" />
    <xsl:call-template name="einzelplanlehrer" />   
    <xsl:call-template name="aufsichtlehrer" />   
  </xsl:for-each>
  <xsl:for-each select="/sp/raeume/ra">
    <xsl:call-template name="kopfraum" />
    <xsl:call-template name="einzelplanraum" />   
  </xsl:for-each>
</xsl:template>

<!-- Klassenplan_______________________________________________________________________________________ -->

<xsl:template name="menuklasse">
  <xsl:for-each select="klassen/kl">
    <div class="menuklassename">
      <xsl:element name="a" use-attribute-sets="linkklasse">
        <xsl:value-of select="kl_kurz"/>
      </xsl:element>
    </div>
  </xsl:for-each>
</xsl:template>

<xsl:template name="kopfklasse">
  <xsl:element name="a" use-attribute-sets="ankerklasse"></xsl:element>
  <br/>
  <span class="spfuer">Stundenplan für Klasse <span class="spfuerkl"><xsl:value-of select="kl_kurz"/></span></span>
  <br/>
  <span class="spschulname">
    <xsl:value-of select="'Stand: '"/>
    <xsl:value-of select="/sp/kopf/datum"/>
    <xsl:value-of select="' '"/>
    <xsl:value-of select="/sp/kopf/schulname"/></span>
    <xsl:value-of select="' '"/>
  <a class="linkseitenanfang" title="Seitenanfang" href="#anfang">&lt;&lt;</a>
  <br/>
</xsl:template>

<xsl:template name="einzelplanklasse">
  <br/>
  <table border="2" class="tableplan">
    <tr>
      <td class="kopfstunde">Stunde<br/>Zeit</td>
      <td class="kopftag">Montag</td>
      <td class="kopftag">Dienstag</td>
      <td class="kopftag">Mittwoch</td>
      <td class="kopftag">Donnerstag</td>
      <td class="kopftag">Freitag</td>
    </tr>
    <xsl:for-each select="kl_stunde">
      <xsl:call-template name="zeileklasse">
        <xsl:with-param name="kl"><xsl:value-of select="../kl_kurz"/></xsl:with-param>
        <xsl:with-param name="st"><xsl:value-of select="."/></xsl:with-param>
        <xsl:with-param name="zeit"><xsl:value-of select="./@kl_zeit"/></xsl:with-param>
      </xsl:call-template>
    </xsl:for-each>
  </table>
</xsl:template>

<xsl:template name="zeileklasse">
  <xsl:param name="kl"/>
  <xsl:param name="st"/>
  <xsl:param name="zeit"/>
  <tr>
    <td class="stunde">
      <xsl:value-of select="$st"/>
      <br/>
      <xsl:value-of select="$zeit"/>
    </td>
    <td>
      <xsl:call-template name="stundeklasse">
        <xsl:with-param name="kl"><xsl:value-of select="$kl"/></xsl:with-param>
        <xsl:with-param name="tg"><xsl:value-of select="'1'"/></xsl:with-param>
        <xsl:with-param name="st"><xsl:value-of select="$st"/></xsl:with-param>
      </xsl:call-template>
    </td>
    <td>
      <xsl:call-template name="stundeklasse">
        <xsl:with-param name="kl"><xsl:value-of select="$kl"/></xsl:with-param>
        <xsl:with-param name="tg"><xsl:value-of select="'2'"/></xsl:with-param>
        <xsl:with-param name="st"><xsl:value-of select="$st"/></xsl:with-param>
      </xsl:call-template>
    </td>
    <td>
      <xsl:call-template name="stundeklasse">
        <xsl:with-param name="kl"><xsl:value-of select="$kl"/></xsl:with-param>
        <xsl:with-param name="tg"><xsl:value-of select="'3'"/></xsl:with-param>
        <xsl:with-param name="st"><xsl:value-of select="$st"/></xsl:with-param>
      </xsl:call-template>
    </td>
    <td>
      <xsl:call-template name="stundeklasse">
        <xsl:with-param name="kl"><xsl:value-of select="$kl"/></xsl:with-param>
        <xsl:with-param name="tg"><xsl:value-of select="'4'"/></xsl:with-param>
        <xsl:with-param name="st"><xsl:value-of select="$st"/></xsl:with-param>
      </xsl:call-template>
    </td>
    <td>
      <xsl:call-template name="stundeklasse">
        <xsl:with-param name="kl"><xsl:value-of select="$kl"/></xsl:with-param>
        <xsl:with-param name="tg"><xsl:value-of select="'5'"/></xsl:with-param>
        <xsl:with-param name="st"><xsl:value-of select="$st"/></xsl:with-param>
      </xsl:call-template>
    </td>
  </tr>
</xsl:template>

<xsl:template name="stundeklasse">
  <xsl:param name="kl"/>
  <xsl:param name="tg"/>
  <xsl:param name="st"/>
  <xsl:if test="count(../kl_sperrung/pl[pl_stunde=$st and pl_tag=$tg])">
    <xsl:attribute name="class">
      <xsl:value-of select="'sperrung'"/> 
    </xsl:attribute>
  </xsl:if>
  <xsl:for-each select="../kl_plan/pl[pl_stunde=$st and pl_tag=$tg]"> 
    <xsl:call-template name="informationklasse" />
  </xsl:for-each>
  <xsl:for-each select="../kl_info/pl[pl_stunde=$st and pl_tag=$tg]"> 
      <xsl:value-of select="pl_un"/> 
  </xsl:for-each>
</xsl:template>

<xsl:template name="stundeklassealt">
  <xsl:param name="kl"/>
  <xsl:param name="tg"/>
  <xsl:param name="st"/>
  <xsl:for-each select="/sp/plan[@tg=$tg]">
    <xsl:for-each select="pl[pl_stunde=$st and pl_tag=$tg and pl_klasse=$kl]"> 
        <xsl:call-template name="informationklasse" />
    </xsl:for-each>
  </xsl:for-each>
</xsl:template>

<xsl:template name="informationklasse">
  <table class="tablestunde">
    <tr>
      <!-- Information Fach oder Gruppe -->
      <td>
        <xsl:choose>
          <xsl:when test="pl_gruppe!=''">
            <xsl:value-of select="pl_gruppe"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:choose>
              <xsl:when test="pl_fach/@fageaendert">
                <span class="fachgeaendert"><xsl:value-of select="pl_fach"/></span>
              </xsl:when>
              <xsl:otherwise>
                <span class="fach"><xsl:value-of select="pl_fach"/></span>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:if test="pl_woche=1">
          <xsl:value-of select="'*'"/> 
        </xsl:if>
        <xsl:if test="pl_woche=2">
          <xsl:value-of select="'**'"/> 
        </xsl:if>
      </td> 

      <!-- Information Lehrer -->
      <td>       
        <xsl:for-each select="pl_lehrer">
          <xsl:element name="a" use-attribute-sets="linkplanle">
            <xsl:choose>
              <xsl:when test="./@legeaendert">
                <span class="lehrergeaendert"><xsl:value-of select="concat(.,' ')"/></span>
              </xsl:when>
              <xsl:otherwise>
                <span class="lehrer"><xsl:value-of select="concat(.,' ')"/></span>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:element>
        </xsl:for-each>
      </td>
      
      <!-- Information Raum -->
      <td>       
        <xsl:for-each select="pl_raum">
          <xsl:element name="a" use-attribute-sets="linkplanra">
            <xsl:choose>
              <xsl:when test="./@rageaendert">
                <span class="raumgeaendert"><xsl:value-of select="concat(.,' ')"/></span>
              </xsl:when>
              <xsl:otherwise>
                <span class="raum"><xsl:value-of select="concat(.,' ')"/></span>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:element>
        </xsl:for-each>
      </td>
      
    </tr>
  </table>
</xsl:template>

<!-- Lehrerplan_______________________________________________________________________________________ -->

<xsl:template name="menulehrer">
  <div class="menulehrer">
    <xsl:for-each select="lehrer/le">
      <div class="menulehrername">
        <xsl:element name="a" use-attribute-sets="linklehrer">
          <xsl:value-of select="le_lang"/>
        </xsl:element>
      </div>
    </xsl:for-each>
  </div>
</xsl:template>

<xsl:template name="kopflehrer">
  <xsl:element name="a" use-attribute-sets="ankerlehrer"></xsl:element>
  <br/>
  <span class="spfuer">Stundenplan für Lehrer <span class="spfuerkl"><xsl:value-of select="le_lang"/></span></span>
  <br/>
  <span class="spschulname">
    <xsl:value-of select="'Stand: '"/>
    <xsl:value-of select="/sp/kopf/datum"/>
    <xsl:value-of select="' '"/>
    <xsl:value-of select="/sp/kopf/schulname"/></span>
    <xsl:value-of select="' '"/>
  <a class="linkseitenanfang" title="Seitenanfang" href="#anfang">&lt;&lt;</a>
  <br/>
</xsl:template>

<xsl:template name="aufsichtlehrer">
  <br/>
    <xsl:for-each select="le_aufsichten">
      <xsl:for-each select="aufsicht">
        <span>
        <xsl:attribute name="class">
          <xsl:choose>
            <xsl:when test="au_info/@augeaendert">
              <xsl:value-of select="'fachgeaendert'"/> 
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="'fach'"/> 
            </xsl:otherwise>
          </xsl:choose>
        </xsl:attribute>

        Aufsicht: <xsl:value-of select="au_info"/>
        </span>
        <br/>
      </xsl:for-each>
    </xsl:for-each>
</xsl:template>

<xsl:template name="einzelplanlehrer">
  <br/>
  <table border="2" class="tableplan">
    <tr>
      <td class="kopfstunde">Stunde<br/>Zeit</td>
      <td class="kopftag">Montag</td>
      <td class="kopftag">Dienstag</td>
      <td class="kopftag">Mittwoch</td>
      <td class="kopftag">Donnerstag</td>
      <td class="kopftag">Freitag</td>
    </tr>
    <xsl:for-each select="le_stunde">
      <xsl:call-template name="zeilelehrer">
        <xsl:with-param name="kl"><xsl:value-of select="../le_kurz"/></xsl:with-param>
        <xsl:with-param name="st"><xsl:value-of select="."/></xsl:with-param>
        <xsl:with-param name="zeit"><xsl:value-of select="./@le_zeit"/></xsl:with-param>
      </xsl:call-template>
    </xsl:for-each>
  </table>
</xsl:template>

<xsl:template name="zeilelehrer">
  <xsl:param name="kl"/>
  <xsl:param name="st"/>
  <xsl:param name="zeit"/>
  <tr>
    <td class="stunde">
      <xsl:value-of select="$st"/>
      <br/>
      <xsl:value-of select="$zeit"/>
    </td>
    <td>
      <xsl:call-template name="stundelehrer">
        <xsl:with-param name="kl"><xsl:value-of select="$kl"/></xsl:with-param>
        <xsl:with-param name="tg"><xsl:value-of select="'1'"/></xsl:with-param>
        <xsl:with-param name="st"><xsl:value-of select="$st"/></xsl:with-param>
      </xsl:call-template>
    </td>
    <td>
      <xsl:call-template name="stundelehrer">
        <xsl:with-param name="kl"><xsl:value-of select="$kl"/></xsl:with-param>
        <xsl:with-param name="tg"><xsl:value-of select="'2'"/></xsl:with-param>
        <xsl:with-param name="st"><xsl:value-of select="$st"/></xsl:with-param>
      </xsl:call-template>
    </td>
    <td>
      <xsl:call-template name="stundelehrer">
        <xsl:with-param name="kl"><xsl:value-of select="$kl"/></xsl:with-param>
        <xsl:with-param name="tg"><xsl:value-of select="'3'"/></xsl:with-param>
        <xsl:with-param name="st"><xsl:value-of select="$st"/></xsl:with-param>
      </xsl:call-template>
    </td>
    <td>
      <xsl:call-template name="stundelehrer">
        <xsl:with-param name="kl"><xsl:value-of select="$kl"/></xsl:with-param>
        <xsl:with-param name="tg"><xsl:value-of select="'4'"/></xsl:with-param>
        <xsl:with-param name="st"><xsl:value-of select="$st"/></xsl:with-param>
      </xsl:call-template>
    </td>
    <td>
      <xsl:call-template name="stundelehrer">
        <xsl:with-param name="kl"><xsl:value-of select="$kl"/></xsl:with-param>
        <xsl:with-param name="tg"><xsl:value-of select="'5'"/></xsl:with-param>
        <xsl:with-param name="st"><xsl:value-of select="$st"/></xsl:with-param>
      </xsl:call-template>
    </td>
  </tr>
</xsl:template>

<xsl:template name="stundelehrer">
  <xsl:param name="kl"/>
  <xsl:param name="tg"/>
  <xsl:param name="st"/>
  <xsl:if test="count(../le_sperrung/pl[pl_stunde=$st and pl_tag=$tg])">
    <xsl:attribute name="class">
      <xsl:value-of select="'sperrung'"/> 
    </xsl:attribute>
  </xsl:if>
  <xsl:for-each select="../le_plan/pl[pl_stunde=$st and pl_tag=$tg]"> 
    <xsl:call-template name="informationlehrer" />
  </xsl:for-each>
  <xsl:for-each select="../le_info/pl[pl_stunde=$st and pl_tag=$tg]"> 
      <xsl:value-of select="pl_un"/> 
  </xsl:for-each>
</xsl:template>

<xsl:template name="informationlehrer">
  <table class="tablestunde">
    <tr>
      <!-- Information Fach oder Gruppe -->
      <td>
        <xsl:attribute name="class">
          <xsl:choose>
            <xsl:when test="pl_fach/@fageaendert">
              <xsl:value-of select="'fachgeaendert'"/> 
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="'fach'"/> 
            </xsl:otherwise>
          </xsl:choose>
        </xsl:attribute>
        <xsl:choose>
          <xsl:when test="pl_gruppe!=''">
            <xsl:value-of select="pl_gruppe"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="pl_fach"/>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:if test="pl_woche=1">
          <xsl:value-of select="'*'"/> 
        </xsl:if>
        <xsl:if test="pl_woche=2">
          <xsl:value-of select="'**'"/> 
        </xsl:if>
      </td> 
      
      <!-- Information Klasse -->
      <td>       
        <xsl:attribute name="class">
          <xsl:value-of select="'klasse'"/> 
        </xsl:attribute>
        <xsl:for-each select="pl_klasse">
          <xsl:element name="a" use-attribute-sets="linkplankl">
            <xsl:value-of select="concat(.,' ')"/>
          </xsl:element>
        </xsl:for-each>
      </td>

      <!-- Information Raum -->
      <td>       
        <xsl:for-each select="pl_raum">
          <xsl:element name="a" use-attribute-sets="linkplanra">
            <xsl:choose>
              <xsl:when test="./@rageaendert">
                <span class="raumgeaendert"><xsl:value-of select="concat(.,' ')"/></span>
              </xsl:when>
              <xsl:otherwise>
                <span class="raum"><xsl:value-of select="concat(.,' ')"/></span>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:element>
        </xsl:for-each>
      </td>
      
    </tr>
  </table>
</xsl:template>

<!-- Raumplan_______________________________________________________________________________________ -->

<xsl:template name="menuraum">
  <div class="menuraum">
    <xsl:for-each select="raeume/ra">
      <div class="menuraumname">
        <xsl:element name="a" use-attribute-sets="linkraum">
          <xsl:value-of select="ra_kurz"/>
        </xsl:element>
      </div>
    </xsl:for-each>
  </div>
</xsl:template>

<xsl:template name="kopfraum">
  <xsl:element name="a" use-attribute-sets="ankerraum"></xsl:element>
  <br/>
  <span class="spfuer">Stundenplan für Raum <span class="spfuerkl"><xsl:value-of select="ra_kurz"/></span></span>
  <br/>
  <span class="spschulname">
    <xsl:value-of select="'Stand: '"/>
    <xsl:value-of select="/sp/kopf/datum"/>
    <xsl:value-of select="' '"/>
    <xsl:value-of select="/sp/kopf/schulname"/></span>
    <xsl:value-of select="' '"/>
  <a class="linkseitenanfang" title="Seitenanfang" href="#anfang">&lt;&lt;</a>
  <br/>
</xsl:template>

<xsl:template name="einzelplanraum">
  <br/>
  <table border="2" class="tableplan">
    <tr>
      <td class="kopfstunde">Stunde<br/>Zeit</td>
      <td class="kopftag">Montag</td>
      <td class="kopftag">Dienstag</td>
      <td class="kopftag">Mittwoch</td>
      <td class="kopftag">Donnerstag</td>
      <td class="kopftag">Freitag</td>
    </tr>
    <xsl:for-each select="ra_stunde">
      <xsl:call-template name="zeileraum">
        <xsl:with-param name="kl"><xsl:value-of select="../ra_kurz"/></xsl:with-param>
        <xsl:with-param name="st"><xsl:value-of select="."/></xsl:with-param>
        <xsl:with-param name="zeit"><xsl:value-of select="./@ra_zeit"/></xsl:with-param>
      </xsl:call-template>
    </xsl:for-each>
  </table>
</xsl:template>

<xsl:template name="zeileraum">
  <xsl:param name="kl"/>
  <xsl:param name="st"/>
  <xsl:param name="zeit"/>
  <tr>
    <td class="stunde">
      <xsl:value-of select="$st"/>
      <br/>
      <xsl:value-of select="$zeit"/>
    </td>
    <td>
      <xsl:call-template name="stunderaum">
        <xsl:with-param name="kl"><xsl:value-of select="$kl"/></xsl:with-param>
        <xsl:with-param name="tg"><xsl:value-of select="'1'"/></xsl:with-param>
        <xsl:with-param name="st"><xsl:value-of select="$st"/></xsl:with-param>
      </xsl:call-template>
    </td>
    <td>
      <xsl:call-template name="stunderaum">
        <xsl:with-param name="kl"><xsl:value-of select="$kl"/></xsl:with-param>
        <xsl:with-param name="tg"><xsl:value-of select="'2'"/></xsl:with-param>
        <xsl:with-param name="st"><xsl:value-of select="$st"/></xsl:with-param>
      </xsl:call-template>
    </td>
    <td>
      <xsl:call-template name="stunderaum">
        <xsl:with-param name="kl"><xsl:value-of select="$kl"/></xsl:with-param>
        <xsl:with-param name="tg"><xsl:value-of select="'3'"/></xsl:with-param>
        <xsl:with-param name="st"><xsl:value-of select="$st"/></xsl:with-param>
      </xsl:call-template>
    </td>
    <td>
      <xsl:call-template name="stunderaum">
        <xsl:with-param name="kl"><xsl:value-of select="$kl"/></xsl:with-param>
        <xsl:with-param name="tg"><xsl:value-of select="'4'"/></xsl:with-param>
        <xsl:with-param name="st"><xsl:value-of select="$st"/></xsl:with-param>
      </xsl:call-template>
    </td>
    <td>
      <xsl:call-template name="stunderaum">
        <xsl:with-param name="kl"><xsl:value-of select="$kl"/></xsl:with-param>
        <xsl:with-param name="tg"><xsl:value-of select="'5'"/></xsl:with-param>
        <xsl:with-param name="st"><xsl:value-of select="$st"/></xsl:with-param>
      </xsl:call-template>
    </td>
  </tr>
</xsl:template>

<xsl:template name="stunderaum">
  <xsl:param name="kl"/>
  <xsl:param name="tg"/>
  <xsl:param name="st"/>
  <xsl:if test="count(../ra_sperrung/pl[pl_stunde=$st and pl_tag=$tg])">
    <xsl:attribute name="class">
      <xsl:value-of select="'sperrung'"/> 
    </xsl:attribute>
  </xsl:if>
  <xsl:for-each select="../ra_plan/pl[pl_stunde=$st and pl_tag=$tg]"> 
    <xsl:call-template name="informationraum" />
  </xsl:for-each>
  <xsl:for-each select="../ra_info/pl[pl_stunde=$st and pl_tag=$tg]"> 
      <xsl:value-of select="pl_un"/> 
  </xsl:for-each>
</xsl:template>

<xsl:template name="informationraum">
  <table class="tablestunde">
    <tr>
      <!-- Information Fach oder Gruppe -->
      <td>
        <xsl:attribute name="class">
          <xsl:choose>
            <xsl:when test="pl_fach/@fageaendert">
              <xsl:value-of select="'fachgeaendert'"/> 
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="'fach'"/> 
            </xsl:otherwise>
          </xsl:choose>
        </xsl:attribute>
        <xsl:choose>
          <xsl:when test="pl_gruppe!=''">
            <xsl:value-of select="pl_gruppe"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="pl_fach"/>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:if test="pl_woche=1">
          <xsl:value-of select="'*'"/> 
        </xsl:if>
        <xsl:if test="pl_woche=2">
          <xsl:value-of select="'**'"/> 
        </xsl:if>
      </td> 
      
      <!-- Information Lehrer -->
      <td>       
        <xsl:for-each select="pl_lehrer">
          <xsl:element name="a" use-attribute-sets="linkplanle">
            <xsl:choose>
              <xsl:when test="./@legeaendert">
                <span class="lehrergeaendert"><xsl:value-of select="concat(.,' ')"/></span>
              </xsl:when>
              <xsl:otherwise>
                <span class="lehrer"><xsl:value-of select="concat(.,' ')"/></span>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:element>
        </xsl:for-each>
      </td>

      <!-- Information Klasse -->
      <td>       
        <xsl:attribute name="class">
          <xsl:value-of select="'klasse'"/> 
        </xsl:attribute>
        <xsl:for-each select="pl_klasse">
          <xsl:element name="a" use-attribute-sets="linkplankl">
            <xsl:value-of select="concat(.,' ')"/>
          </xsl:element>
        </xsl:for-each>
      </td>

    </tr>
  </table>
</xsl:template>

<!-- Stunde_______________________________________________________________________________________ -->

<xsl:template name="menustunde">
  <xsl:for-each select="zeitraster/zr_stunde">
    <div class="menustunde">
      <xsl:element name="a" use-attribute-sets="linkstunde">
        <xsl:value-of select="."/><xsl:value-of select="'.'"/>
      </xsl:element>
      <xsl:value-of select="' ('"/>
      <xsl:value-of select="./@zr_zeit"/>
      <xsl:value-of select="')'"/>
    </div>
  </xsl:for-each>
</xsl:template>

<xsl:template name="kopfstunde">
  <xsl:element name="a" use-attribute-sets="ankerstunde"/>
  <br/>
  <span class="datum"><xsl:value-of select="/sp/kopf/datum"/></span>
  <xsl:value-of select="' - '"/>
  <span class="spfuerst"><xsl:value-of select="."/>. Stunde</span>
  <xsl:value-of select="' ('"/>
  <xsl:value-of select="./@zr_zeit"/>
  <xsl:value-of select="') '"/>
  <a class="linkseitenanfang" title="Seitenanfang" href="#anfang">&lt;&lt;</a>
  <br/>
</xsl:template>

<xsl:template name="einzelplanstunde">
  <xsl:for-each select=".">
    <xsl:call-template name="stundestunde">
      <xsl:with-param name="tg"><xsl:value-of select="/sp/kopf/tag"/></xsl:with-param>
      <xsl:with-param name="st"><xsl:value-of select="."/></xsl:with-param>
      <xsl:with-param name="wo"><xsl:value-of select="/sp/kopf/woche"/></xsl:with-param>
    </xsl:call-template>
  </xsl:for-each>
  <div class="clear"/>
</xsl:template>

<xsl:template name="stundestunde">
  <xsl:param name="tg"/>
  <xsl:param name="st"/>
  <xsl:param name="wo"/>
  <xsl:for-each select="/sp/plan[@tg=$tg]">
    <xsl:for-each select="pl[pl_stunde=$st and pl_tag=$tg and (pl_woche=$wo or count(pl_woche)=0)]"> 
      <xsl:sort select="pl_lehrer"/>
      <xsl:call-template name="informationstunde" />
    </xsl:for-each>
  </xsl:for-each>
</xsl:template>

<xsl:template name="informationstunde">
  <div class="stue">
    <!-- Information Fach oder Gruppe -->
    <div class="stfach">
      <xsl:choose>
        <xsl:when test="pl_gruppe!=''">
          <xsl:value-of select="pl_gruppe"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:choose>
            <xsl:when test="pl_fach/@fageaendert">
              <span class="fachgeaendert"><xsl:value-of select="pl_fach"/></span>
            </xsl:when>
            <xsl:otherwise>
              <span class="fach"><xsl:value-of select="pl_fach"/></span>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:if test="pl_woche=1">
        <xsl:value-of select="'*'"/> 
      </xsl:if>
      <xsl:if test="pl_woche=2">
        <xsl:value-of select="'**'"/> 
      </xsl:if>
    </div>

    <!-- Information Lehrer -->
    <div class="stlehrer">
      <xsl:for-each select="pl_lehrer">
        <xsl:element name="a" use-attribute-sets="linkplanle">
        <xsl:choose>
          <xsl:when test="./@legeaendert">
            <span class="lehrergeaendert" title="Lehrerplan aufrufen"><xsl:value-of select="concat(.,' ')"/></span>
          </xsl:when>
          <xsl:otherwise>
            <span class="lehrer" title="Lehrerplan aufrufen"><xsl:value-of select="concat(.,' ')"/></span>
          </xsl:otherwise>
        </xsl:choose>
        </xsl:element>
      </xsl:for-each>
    </div>

      <!-- Information Raum -->
    <div class="straum">
        <xsl:for-each select="pl_raum">
          <xsl:element name="a" use-attribute-sets="linkplanra">
            <xsl:choose>
              <xsl:when test="./@rageaendert">
                <span class="raumgeaendert"><xsl:value-of select="concat(.,' ')"/></span>
              </xsl:when>
              <xsl:otherwise>
                <span class="raum"><xsl:value-of select="concat(.,' ')"/></span>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:element>
        </xsl:for-each>
    </div>

    <!-- Information Klasse -->
    <div class="stklasse">
      <xsl:for-each select="pl_klasse">
        <xsl:element name="a" use-attribute-sets="linkplankl">
          <span class="klasse" title="Klassenplan aufrufen"><xsl:value-of select="concat(.,' ')"/></span>
        </xsl:element>
      </xsl:for-each>
    </div>
  </div>
</xsl:template>

</xsl:stylesheet>