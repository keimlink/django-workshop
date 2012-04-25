import cStringIO as StringIO

from django.http import HttpResponse
from django.views.generic import DetailView
import ho.pisa as pisa


class PDFView(DetailView):
    def render_to_pdf(self, html):
        pdf = StringIO.StringIO()
        pisa.CreatePDF(html, pdf, encoding='utf-8')
        pdf.seek(0)
        return pdf

    @property
    def filename(self):
        return getattr(self.get_object(), self.slug_field)

    def render_to_response(self, context, **response_kwargs):
        tpl = super(PDFView, self).render_to_response(context, **response_kwargs)
        tpl.render()
        pdf = self.render_to_pdf(tpl.rendered_content)
        response = HttpResponse(pdf, mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s.pdf' % self.filename
        return response
