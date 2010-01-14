<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">

    <xsl:template match="/igt">
        <html>
            <body>
            <xsl:apply-templates select="clause"/>
            </body>
        </html>
    </xsl:template>


    <!--main template for processing clauses-->
    <xsl:template match="clause">

        <h3>IGT Instance</h3>
         <pre>
                    
        <xsl:call-template name="findRep">
            <xsl:with-param name="current_idref" select="@representation"/>
        </xsl:call-template>
        
             <xsl:text> &#10; </xsl:text>
        
        <xsl:for-each select="synword/morpheme">
                    
            <xsl:value-of select="@gloss"/>
            <xsl:text> </xsl:text>

         </xsl:for-each>
             <xsl:text> &#10; </xsl:text>
             
             
            <!--call to find the translation -->

             <xsl:call-template name="findTrans">
                 <xsl:with-param name="source" select="@representation"/>
             </xsl:call-template>


         </pre>
    </xsl:template>

    <!-- This function returns a representation given an id -->
    <xsl:template name="findRep">
        <xsl:param name="current_idref"/>
        
        <xsl:for-each select="/igt/representation">
            <xsl:if test="@id=$current_idref">
                <xsl:value-of select="."/>
            </xsl:if>
         </xsl:for-each>
    </xsl:template>

    <!-- This function returns the translation for a given unit -->
    <xsl:template name="findTrans">
        <xsl:param name="source"/>
        
        <xsl:for-each select="/igt/translation">
            <xsl:if test="$source=@source">
                
                <xsl:call-template name="findRep">
                    <xsl:with-param name="current_idref" select="@target"/>
                </xsl:call-template>
                
            </xsl:if>
        </xsl:for-each>
    </xsl:template>


</xsl:stylesheet>
